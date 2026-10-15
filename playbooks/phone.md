# Phone and device films — أفلام الهاتف والأجهزة

A phone film sells a screen by giving it a body: a device with mass, a light source and a surface it sits on, so that every tap, swipe and turn reads as something a hand could do. This playbook covers 3D and 2.5D phone mockups, screen perspective, touch gestures, device rotation, safe crops, the notch and dynamic island, reflections and shadows. It is written for Claude Code building editable motion with the KOSIF starters, and it supplies numbers, not adjectives.

فيلم الهاتف يبيع الشاشة بأن يمنحها جسدًا: جهاز له كتلة ومصدر ضوء وسطح يستقر عليه، فتُقرأ كل نقرة وسحبة ودورة كحركة يد حقيقية. يغطي هذا الدليل مجسمات الهاتف ثلاثية وشبه ثلاثية الأبعاد، منظور الشاشة، إيماءات اللمس، دوران الجهاز، القصّ الآمن، النوتش والجزيرة الديناميكية، الانعكاسات والظلال، بأرقام محددة لا بصفات عامة.

## 1. When to use — متى تستخدمه

Use this playbook when the deliverable is about an app, a mobile website, a feature inside a screen, or a product that lives on a handheld device: launch films, feature tours, App Store previews, UGC-style promos with a device insert, and explainers where a chat, feed or dashboard is the evidence. It also applies to tablets and watches with the same rules scaled.

Do not reach for a phone mockup when the screen content is the only thing that matters and the device would just steal pixels (a full-bleed UI walkthrough belongs to `playbooks/product-ui.md`), when the request is a data story (`playbooks/charts.md`), or when the brief asks for a true 3D product shot with materials and lighting that CSS cannot fake (`playbooks/3d.md`, Three.js). A device film is the right call when the physicality of the phone carries meaning: holding, turning, tapping, pulling the phone out of a pocket, two phones talking to each other.

**بالعربية:** استخدم هذا الدليل عندما يكون موضوع الفيلم تطبيقًا أو موقعًا على الجوال أو ميزة داخل شاشة. لا تستخدم مجسم الهاتف إذا كانت الشاشة وحدها هي المهمة (دليل واجهات المنتج)، أو إذا كان المطلوب قصة بيانات (دليل الرسوم البيانية)، أو لقطة منتج ثلاثية الأبعاد حقيقية بخامات وإضاءة (دليل 3D). الجهاز يستحق مكانه فقط حين تحمل جسديته معنى: الإمساك، الدوران، النقر، هاتفان يتبادلان.

## 2. Visual grammar — القواعد البصرية

**One device system.** Build the phone from a few constants and never eyeball them twice: a screen of 390×844 logical px (19.5:9), a screen corner radius of 12–14 % of the screen width, a bezel of 2–3 % of the screen width, and a frame radius equal to screen radius plus bezel so the two curves stay concentric. A dynamic island is a 120×36 pill, 12 px below the screen top; a classic notch is 210×34 with a 20 px bottom radius. Pick one and keep it on every shot.

**Screen as real UI.** The screen is a clipped container holding live DOM, SVG or Canvas drawing at 2× pixel density, not a blurred screenshot. Rendered in-screen text must stay at or above 30 px when the comp is 1080 wide; any sentence that carries the message goes outside the device as a callout at 36 px or larger. The island and the home indicator are painted after the UI so they never scroll with it.

**Perspective.** For a 1080-wide comp use a perspective distance of 1200–1600 px (roughly 1.3× the comp width). Yaw is limited to ±28° and pitch to ±8°; beyond that, the screen text becomes unreadable and the frame starts to look like a card. A resting pose is never dead-on 0°: hold at −6° to −10° yaw so one edge of the frame shows and the device keeps a 2.5D identity.

**Light, shadow, reflection.** One key light, top-left by default. Three things must agree with it: the shadow offset (down 40–60 px, and horizontally against the yaw, roughly −yaw × 1.6 px), the 1 px inner highlight on the lit edge of the frame, and the reflection band, a soft diagonal gradient at 10–16 % white opacity that crosses the glass once while the device turns. If the phone sits on a surface, add a contact shadow: a short ellipse, 8–12 px blur, 35 % opacity, directly under the lower edge. Ambient shadow is 60–100 px blur at 50 % opacity.

**Scale and placement.** In 9:16 the device fills 55–70 % of the frame height; in 16:9 it fills 75–85 % and sits on a third line, leaving the other two-thirds for type. In 1:1 use 70 % height and let the hero text live above or below the device.

**Safe crops.** Keep the 5 % side and 12 % top-bottom safe margins for any text, including callouts. A device may bleed off the bottom edge in 9:16 when the bottom 20 % of the screen is non-essential. Never cut the frame through the island, the camera or the home indicator. When you push in on screen content, keep at least one full vertical edge of the frame visible so the viewer still knows they are looking at a phone.

**بالعربية:** ابنِ الهاتف من ثوابت: شاشة 390×844، نصف قطر زاوية الشاشة 12–14 % من عرضها، إطار 2–3 %، ونصف قطر الإطار = نصف قطر الشاشة + الإطار. الجزيرة 120×36 على بعد 12 بكسل من أعلى الشاشة. الشاشة واجهة حقيقية مقصوصة لا لقطة مموهة، ونص الشاشة ≥ 30 بكسل عند عرض 1080، والنص الذي يحمل الرسالة يخرج خارج الجهاز بحجم ≥ 36. المنظور 1200–1600 بكسل، الدوران الأفقي ≤ ±28° والرأسي ≤ ±8°، ووضع الراحة −6° إلى −10° لا صفر. مصدر ضوء واحد يتفق معه الظل (نزول 40–60 بكسل وعكس اتجاه الدوران)، والحافة المضيئة، وشريط الانعكاس (بياض 10–16 %) الذي يعبر الزجاج مرة واحدة. لا تقطع الإطار عبر الجزيرة أو مؤشر الرئيسية، واحتفظ بحافة عمودية كاملة ظاهرة عند التقريب.

## 3. Motion mechanics — ميكانيكا الحركة

- **Entrance:** 700–900 ms. Rise 120–160 px while yaw settles from −22° to −8° and opacity goes 0→1 in the first 250 ms. Easing: `cubic-bezier(0.16, 1, 0.3, 1)` or a spring `{ damping: 18, stiffness: 90, mass: 1.1 }`.
- **Rotation speed:** up to 40°/s during a reveal or turn-table, 4°/s or less during an idle drift. Overshoot on settle is 1–2°, never more. Never cross through exactly 0° at the end of a move.
- **Idle hover:** amplitude ≤ 6 px, period ≥ 3.2 s, sine. Anything faster or larger reads as a bobbing template.
- **Tap:** press 90 ms with `cubic-bezier(0.4, 0, 1, 1)` to 0.96 scale on the device (or 0.92 on the tapped button); release with a spring `{ stiffness: 240, damping: 14 }`; a ripple ring grows 0→64 px while fading 0.6→0 over 300 ms. A visible cue (fingertip, ring or cursor dot) appears 60 ms before the press.
- **Swipe / screen transition:** 420–520 ms, `cubic-bezier(0.2, 0.8, 0.2, 1)`. The incoming screen travels the full width from the inline-end side; the outgoing screen moves 30 % of the distance and dims to 60 % (parallax). Vertical modal sheets: 380 ms up with the same curve, 300 ms down with `cubic-bezier(0.4, 0, 0.2, 1)`.
- **Scroll:** one card per beat: 450 ms move of about 62 % of the screen height, then a hold of at least 600 ms. Never a linear scroll longer than 2 s. The device counter-rotates 2° against each scroll so the body reacts to the thumb.
- **Stagger:** UI rows 60–90 ms apart; a callout outside the device appears 120 ms after the element it describes; leader lines draw in 260 ms with `cubic-bezier(0.16, 1, 0.3, 1)`.
- **Camera:** slow push 1.00→1.06 over 3–4 s with ease-in-out sine during holds; a dolly on tap 1.00→1.12 in 600 ms centred on the tapped element, then back over 900 ms.
- **Dynamic island:** expand width 120→300 and height 36→80 with a spring `{ stiffness: 180, damping: 16 }` (about 260 ms); content fades in from 180 ms with a 60 ms stagger; collapse in 300 ms.
- **Reflection:** one pass per rotation, 1.2 s, `cubic-bezier(0.33, 1, 0.68, 1)`, peak 0.12–0.16 opacity. It never loops.
- **Shadow:** recomputed every frame from the yaw and the lift; when the device rises 140 px the shadow blur grows by 30 % and its opacity falls by 20 %.

**بالعربية:** الدخول 700–900 ms بمنحنى `cubic-bezier(0.16, 1, 0.3, 1)` أو نابض (تخميد 18، صلابة 90). سرعة الدوران ≤ 40°/ث في الكشف و≤ 4°/ث في السكون، وتجاوز الاستقرار 1–2° فقط. التحويم ≤ 6 بكسل بدورة ≥ 3.2 ث. النقرة: ضغط 90 ms إلى مقياس 0.96 ثم نابض (صلابة 240، تخميد 14) وحلقة 300 ms، مع مؤشر مرئي قبل الضغط بـ 60 ms. السحب 420–520 ms والشاشة الخارجة تتحرك 30 % وتخفت إلى 60 %. التمرير بطاقة لكل نبضة: 450 ms حركة ثم ≥ 600 ms توقف. التدرج بين الصفوف 60–90 ms. الكاميرا دفع بطيء 1.00→1.06 خلال 3–4 ث. الجزيرة تتمدد بنابض (صلابة 180، تخميد 16) وتنكمش في 300 ms. الانعكاس مرة واحدة لكل دوران ولا يتكرر. الظل يُحسب من الدوران والارتفاع كل إطار.

## 4. Scene recipes — وصفات المشاهد

### A. Hero reveal — كشف الجهاز

| start (ms) | end (ms) | action | easing |
|---|---|---|---|
| 0 | 900 | device rises 140 px, yaw −22°→−8°, opacity 0→1 (first 250 ms) | spring damping 18, stiffness 90 |
| 350 | 1550 | reflection band crosses the glass once | cubic-bezier(0.33, 1, 0.68, 1) |
| 600 | 1300 | in-screen UI staggers in (header, then rows every 70 ms) | cubic-bezier(0.2, 0.8, 0.2, 1) |
| 1200 | 1800 | headline outside the device, word by word | spring damping 14, stiffness 120 |
| 900 | 4000 | hold: push 1.00→1.04, yaw drift ±1.5° | ease-in-out sine |

### B. Tap and screen change — نقرة وانتقال شاشة

| start (ms) | end (ms) | action | easing |
|---|---|---|---|
| −60 | 0 | tap cue appears over the target | linear fade |
| 0 | 90 | press: device scale 1→0.96, button 1→0.92 | cubic-bezier(0.4, 0, 1, 1) |
| 90 | 400 | release spring; ripple ring 0→64 px, opacity 0.6→0 | spring stiffness 240, damping 14 |
| 120 | 560 | new screen slides in from the inline-end; old screen parallax 30 %, dims to 60 % | cubic-bezier(0.2, 0.8, 0.2, 1) |
| 120 | 720 | camera dolly 1.00→1.12 centred on the tapped element | cubic-bezier(0.16, 1, 0.3, 1) |
| 560 | 820 | callout leader line draws, label fades in | cubic-bezier(0.16, 1, 0.3, 1) |

### C. Feed scroll with callouts — تمرير مع تعليقات

| start (ms) | end (ms) | action | easing |
|---|---|---|---|
| 0 | 450 | content scrolls one card (62 % of screen height); device yaw −8°→−10° | cubic-bezier(0.2, 0.8, 0.2, 1) |
| 450 | 1150 | hold; current card lifts 6 px and brightens 8 %; callout appears at 570 ms | cubic-bezier(0.16, 1, 0.3, 1) |
| 1150 | 1600 | next scroll; yaw returns to −8° | same as row 1 |
| per beat | | repeat on the beat grid or on sentence starts; stop after at most 5 cards | |

### D. Turn-table handoff between two devices — تسليم بين جهازين

| start (ms) | end (ms) | action | easing |
|---|---|---|---|
| 0 | 1400 | device A yaw −8°→+28° and slides 220 px to the inline-end; device B enters from behind, yaw +30°→+8°, scale 0.9→1 | cubic-bezier(0.65, 0, 0.35, 1) |
| 0 | 1400 | both shadows slide against their yaw every frame | computed |
| 500 | 700 | specular peak on A as it passes the light | linear |
| 700 | 1000 | shared element (a card or avatar) flies from A to B along an arc | cubic-bezier(0.2, 0.8, 0.2, 1) |
| 1400 | 2000 | settle with 1.5° overshoot on both | spring damping 16, stiffness 100 |

### E. Dynamic island notification — إشعار الجزيرة

| start (ms) | end (ms) | action | easing |
|---|---|---|---|
| 0 | 260 | pill expands 120×36 → 300×80 | spring stiffness 180, damping 16 |
| 180 | 420 | icon, title and line stagger in at 60 ms | cubic-bezier(0.16, 1, 0.3, 1) |
| 420 | 2400 | hold; progress or waveform animates inside | linear |
| 2400 | 2700 | collapse back to 120×36 | cubic-bezier(0.4, 0, 0.2, 1) |

**بالعربية:** خمس وصفات جاهزة: كشف الجهاز (دخول 900 ms ثم انعكاس واحد ثم واجهة متدرجة ثم عنوان)، نقرة وانتقال (مؤشر قبل الضغط بـ 60 ms، ضغط 90، نابض، شاشة جديدة خلال 440 ms، تعليق بعدها)، تمرير بطاقة لكل نبضة مع توقف ≥ 600 ms وتعليق جانبي، تسليم بين جهازين خلال 1400 ms مع ذروة لمعان وعنصر مشترك يطير بينهما، وإشعار الجزيرة (تمدد 260 ms، ثبات، انكماش 300 ms). اجعل جداول التوقيت هذه هي مرجع PLAN.md.

## 5. Implementation — التنفيذ

Both starters treat time as the only input: the Remotion starter derives everything from `useCurrentFrame()`, and `starters/html-canvas` draws the frame for `t` inside `window.__kosif.seek(t)` so that `tools/render_html.cjs` can render in seek mode. No `requestAnimationFrame`, `Date.now()` or CSS transitions drive a device; they are not reproducible frame by frame. If you must use CSS animations, render with `--mode virtual`.

**Remotion / React.** Drop this next to `starters/remotion/src/Film.tsx` and give it a `screen` subtree (your UI) and a `tapAt` frame. It reuses `easing.ts` from the starter and belongs inside the `CameraRig` so the whole film shares one camera.

```tsx
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { easeOutExpo, progress } from "./easing";

const W = 390, H = 844, R = 52, BEZEL = 12; // logical px; scale the parent group to taste

export const Device: React.FC<{ screen: React.ReactNode; tapAt?: number }> = ({ screen, tapAt = -1 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 18, stiffness: 90, mass: 1.1 } });
  const yaw = interpolate(enter, [0, 1], [-22, -8]);               // settles off-axis, never 0°
  const lift = interpolate(enter, [0, 1], [140, 0]);
  const tap = tapAt >= 0 ? Math.min(1, spring({ frame: frame - tapAt, fps, config: { damping: 14, stiffness: 240 } })) : 0;
  const press = 1 - 0.04 * Math.sin(Math.PI * tap);                  // dips to 0.96 and returns
  const glare = progress(frame, 10, 36, easeOutExpo);                // one pass, then it rests
  const shadowX = -yaw * 1.6;                                        // shadow opposes the turn
  return (
    <AbsoluteFill style={{ perspective: 1400, justifyContent: "center", alignItems: "center" }}>
      <div style={{
        width: W + 2 * BEZEL, height: H + 2 * BEZEL, borderRadius: R + BEZEL, background: "#15171c",
        position: "relative", overflow: "hidden",
        transform: `translateY(${lift}px) rotateY(${yaw}deg) rotateX(4deg) scale(${press})`,
        boxShadow: `${shadowX}px 48px 90px rgba(0,0,0,0.55), inset 1px 1px 0 rgba(255,255,255,0.09)`,
      }}>
        <div style={{ position: "absolute", inset: BEZEL, borderRadius: R, overflow: "hidden", background: "#000" }}>
          {screen}
          {/* island: painted after the UI so it never scrolls with it */}
          <div style={{ position: "absolute", top: 12, left: "50%", marginLeft: -60, width: 120, height: 36,
            borderRadius: 18, background: "#000" }} />
          {/* reflection: one soft diagonal band crossing the glass during the turn */}
          <div style={{ position: "absolute", inset: 0,
            background: "linear-gradient(115deg, transparent 40%, rgba(255,255,255,0.14) 50%, transparent 60%)",
            transform: `translateX(${interpolate(glare, [0, 1], [-W, W])}px)` }} />
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

**Canvas (starters/html-canvas).** True `rotateY` does not exist on a 2D context, so the 2.5D trick is a width squash by `cos(yaw)` plus a small vertical shear, which is enough below 28°. Call `drawPhone(ctx, t, screenCanvas)` from the starter's `seek(t)` after clearing the frame; `screenCanvas` is an offscreen canvas where the UI is drawn at 2×.

```js
const W = 1080, H = 1920, PHONE = { w: 420, h: 900, r: 60, bezel: 12 };
const expoOut = (t) => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t));
const win = (t, start, len, ease = expoOut) => ease(Math.min(1, Math.max(0, (t - start) / len)));
const rr = (ctx, x, y, w, h, r) => { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); ctx.closePath(); };

function drawPhone(ctx, t, screenCanvas) {
  const enter = win(t, 0, 0.9);                                  // 900 ms entrance
  const yaw = -22 + 14 * enter;                                  // degrees, -22 -> -8
  const rad = (yaw * Math.PI) / 180;
  const float = 6 * Math.sin((t / 3.2) * 2 * Math.PI);           // idle hover: 6 px, 3.2 s
  const cx = W / 2, cy = H / 2 + 140 * (1 - enter) + float;
  const s = PHONE, sx = -s.w / 2 + s.bezel, sy = -s.h / 2 + s.bezel, sw = s.w - 2 * s.bezel, sh = s.h - 2 * s.bezel;
  ctx.save();
  ctx.translate(cx, cy);
  ctx.transform(Math.cos(rad), Math.sin(rad) * 0.12, 0, 1, 0, 0); // 2.5D: squash width, shear edges
  ctx.shadowColor = "rgba(0,0,0,0.55)"; ctx.shadowBlur = 90;      // ambient shadow opposes the yaw
  ctx.shadowOffsetX = -yaw * 1.6; ctx.shadowOffsetY = 48;
  ctx.fillStyle = "#15171c";
  rr(ctx, -s.w / 2, -s.h / 2, s.w, s.h, s.r + s.bezel); ctx.fill();
  ctx.shadowColor = "transparent";
  rr(ctx, sx, sy, sw, sh, s.r); ctx.clip();                       // everything below is on the glass
  ctx.drawImage(screenCanvas, sx, sy, sw, sh);
  ctx.fillStyle = "#000"; rr(ctx, -60, sy + 12, 120, 36, 18); ctx.fill(); // island stays put
  const glare = win(t, 0.35, 1.2);                                 // one diagonal pass during the turn
  const gx = sx + (glare * 2 - 1) * sw;
  const g = ctx.createLinearGradient(gx, sy, gx + sw * 0.6, sy + sh);
  g.addColorStop(0, "rgba(255,255,255,0)"); g.addColorStop(0.5, "rgba(255,255,255,0.14)"); g.addColorStop(1, "rgba(255,255,255,0)");
  ctx.fillStyle = g; ctx.fillRect(sx, sy, sw, sh);
  ctx.restore();
}
```

Mapping to the starters: in Remotion the `Device` is one `Sequence` child inside `CameraRig`, taps are frames computed from `words.json` (`Math.round(start * fps)`), and screens are plain React components. In html-canvas the timeline is a list of `{ start, len, draw }` windows evaluated by `seek(t)`; `drawPhone` is one of them, `screenCanvas` is updated from the same `t`, and the renderer calls `seek` for every frame at `1 / fps` steps, so there is no drift. Preview with `node tools/render_html.cjs --in index.html --out preview.mp4 --preview` before the final render.

**بالعربية:** الزمن هو المدخل الوحيد: في Remotion كل شيء من `useCurrentFrame()`، وفي html-canvas كل إطار يُرسم داخل `window.__kosif.seek(t)` ليستطيع `tools/render_html.cjs` الرندر بوضع seek. لا تقود الجهاز بـ `requestAnimationFrame` أو `Date.now()` أو انتقالات CSS، وإن اضطررت فاستخدم `--mode virtual`. مقتطف Remotion يضع الجهاز داخل `CameraRig` ويأخذ الشاشة كـ children ولحظة النقر كإطار؛ ومقتطف Canvas يحاكي الدوران بضغط العرض على `cos(yaw)` مع قصّ طفيف، ويرسم الظل والزجاج والجزيرة والانعكاس بالترتيب داخل `clip`.

## 6. Arabic and RTL notes — ملاحظات العربية

- The UI inside the screen is a real RTL layout: `dir="rtl"` on the screen root, logical CSS properties (`marginInlineStart`, `insetInlineEnd`), text aligned to the start. On Canvas set `ctx.direction = "rtl"` and `ctx.textAlign = "right"`, and draw whole words; never split Arabic into letters to animate them (see `playbooks/arabic-typography.md`).
- Mirror the interactions, not the hardware. A back chevron points to the right, a new screen pushes in from the left (the inline-end in RTL), tabs read right to left, a toggle's "on" state sits on the left. The island, the camera, the buttons and the home indicator are physical and never mirror.
- Digits: use the numeral style the brand uses and keep it the same inside and outside the device; a phone number or a time stays LTR as a unit with `unicode-bidi: plaintext`.
- Place hero copy to the right of the device in 16:9 and 1:1 so the eye travels right to left into the screen; rotate the device so its right edge comes nearer (positive yaw) when the text is on the right.
- Callouts attach their leader line to the start of the label (its right end) and the label is right-aligned; a callout about a list row points at the row's start side.
- Use UI fonts with full Arabic coverage (Noto Sans Arabic, IBM Plex Sans Arabic, Cairo) at the same optical size as the Latin fallback; Arabic needs about 10 % more line height inside compact UI rows.

**بالعربية:** الواجهة داخل الشاشة RTL حقيقية: `dir="rtl"` وخصائص CSS منطقية، وعلى Canvas اضبط `ctx.direction = "rtl"` وارسم الكلمة كاملة ولا تفككها. اعكس التفاعل لا العتاد: سهم الرجوع لليمين، الشاشة الجديدة تدخل من اليسار، التبويبات من اليمين لليسار، أما الجزيرة والأزرار ومؤشر الرئيسية فلا تنعكس. الأرقام بنمط واحد داخل الجهاز وخارجه، والأرقام والأوقات وحدة LTR بـ `unicode-bidi: plaintext`. ضع النص الرئيسي يمين الجهاز وأدر الجهاز بحيث تقترب حافته اليمنى. خطوط عربية كاملة التغطية مع ارتفاع سطر أكبر بنحو 10 %.

## 7. Audio sync — المزامنة مع الصوت

The supplied voice is the master clock and is never trimmed or re-timed. Load `words.json` (`start`, `end` in seconds, `emphasis` flag) and derive device events from it:

- A **tap** lands on the onset of the emphasis word: press starts at `start − 40 ms` so the visual change reads with the consonant, and the new screen finishes sliding before `end`. Measure the gap in the test report; the tolerance is 100 ms on every emphasis word.
- A **rotation or turn-table** spans a phrase: begin at the first word of the sentence and reach the settle on its stressed word, never in the middle of a word.
- **Scroll steps** follow sentence starts when there is narration, or the beat grid when there is music (see `playbooks/music.md`); one card per beat, never more than one per 450 ms.
- **Island expansions** are the natural home for a notification sound or a name the narrator says; expand on the word start, collapse 300 ms after the sentence ends.
- SFX are optional and only when requested or licensed: a 30–50 ms click at −18 dBFS on taps, a swipe whoosh of at most 250 ms, both ducked 10 dB under voice. Final mix at −14 LUFS, true peak ≤ −1 dBTP, as in `templates/TEST_REPORT.md`.
- Keep a 100 ms quiet zone before each emphasis word with no new device keyframe other than the one that answers it, so the ear and the eye get one event at a time.

**بالعربية:** الصوت المرفق هو الساعة الرئيسية ولا يُقص ولا يُزاح. من `words.json` تُشتق الأحداث: النقرة تبدأ قبل الكلمة المؤكَّدة بـ 40 ms وتكتمل الشاشة الجديدة قبل نهايتها بتسامح ≤ 100 ms؛ الدوران يمتد على جملة ويستقر على كلمتها المشددة؛ التمرير على بدايات الجمل أو على النبضات؛ الجزيرة تتمدد مع بداية الكلمة وتنكمش بعد الجملة بـ 300 ms. المؤثرات اختيارية ومرخصة فقط: نقرة 30–50 ms عند −18 dBFS، سحبة ≤ 250 ms، مع خفض 10 dB تحت الصوت، والمزج النهائي −14 LUFS. اترك 100 ms هدوء بصري قبل كل كلمة مؤكدة.

## 8. Quality checklist — قائمة الفحص

1. Does the device use one constant set (screen size, radii, bezel, island) on every shot?
2. Is the rest pose off-axis (−6° to −10° yaw) and is yaw never beyond ±28°?
3. Do the shadow offset, the lit edge and the reflection band all agree with one light direction?
4. Does the shadow change when the device lifts or turns, instead of staying a static blob?
5. Is every tap preceded by a visible cue and followed by a real screen state change within 560 ms?
6. Is the screen content live UI at 2× density with in-screen text at or above 30 px at 1080 width?
7. Are the island and the home indicator fixed while the content scrolls underneath?
8. Does every crop keep the island and the home indicator uncut and at least one full vertical edge visible?
9. Is the in-screen UI genuinely RTL (direction, back chevron, push direction) with Arabic words kept whole?
10. Does every emphasis word in `words.json` have a device event within 100 ms, measured and recorded in TEST_REPORT.md?

**بالعربية:** عشرة أسئلة نعم/لا: ثوابت الجهاز واحدة في كل لقطة؟ وضع الراحة مائل والدوران ≤ ±28°؟ الظل والحافة المضيئة والانعكاس من مصدر ضوء واحد؟ الظل يتغير مع الرفع والدوران؟ لكل نقرة مؤشر قبلها وتغيير شاشة بعدها خلال 560 ms؟ الشاشة واجهة حية بدقة 2× ونص ≥ 30 بكسل؟ الجزيرة ومؤشر الرئيسية ثابتان أثناء التمرير؟ القصّ لا يمر عبر الجزيرة ويبقي حافة عمودية كاملة؟ الواجهة RTL حقيقية والكلمات العربية كاملة؟ لكل كلمة مؤكدة حدث خلال 100 ms مقاس في تقرير الفحص؟

## 9. Anti-patterns — أخطاء شائعة

- **The floating phone.** A device with no shadow, no surface and no light direction, hovering in a gradient void. It is the single most recognisable "AI look" in device films.
- **The perpetual bob.** A 20 px sine hover every 1.5 s, forever. Hover is ≤ 6 px and ≥ 3.2 s, and it stops when something else moves.
- **Bending glass.** Yaw beyond 30°, or a 2.5D shear applied to a screenshot, so the screen looks like a sticker peeling off a card.
- **Mismatched curves.** Screen radius and frame radius that are not concentric; the bezel visibly thickens in the corners.
- **The blurry screenshot.** A 1× image stretched into the screen, with text that no viewer can read on a phone.
- **Ghost taps.** Screens that change with no cue, no press and no ripple; the viewer cannot tell what caused what.
- **Looping glare.** A reflection band sweeping the glass every two seconds like a cleaning cycle. One pass per turn.
- **Rainbow chrome.** Multi-stop gradient frames, neon rim lights and glassmorphism on everything, including the shadow.
- **Mirrored hardware.** Flipping the whole device for RTL so the island, the buttons and the camera swap sides, while the UI inside stays LTR.
- **Linear scrolling.** A feed that scrolls continuously for five seconds with nothing to look at; scroll in cards with holds.
- **Wall-clock motion.** `requestAnimationFrame` or CSS transitions driving the device, so the preview and the render disagree.

**بالعربية:** تجنب الهاتف الطائر بلا ظل ولا سطح ولا اتجاه ضوء، والتحويم الدائم السريع، وثني الزجاج بدوران > 30°، والأقواس غير المتمركزة بين الشاشة والإطار، واللقطة المموهة بدقة 1×، والنقرات الشبحية بلا مؤشر، والانعكاس المتكرر كدورة تنظيف، وإطارات الكروم القوسية والزجاجية على كل شيء، وعكس العتاد كله للعربية بينما الواجهة داخله تبقى LTR، والتمرير الخطي الطويل، وتحريك الجهاز بساعة المتصفح بدل زمن الإطار.

## 10. Related styles — استايلات ذات صلة

- pm-twoclipping-221cab — Photo print app launch film
- pm-twoclipping-6dd14e — UGC ad generator promo
- pm-dale-vaz-cc612a — Sahi trading terminal reveal
- pm-deifosv-04e4d3 — Tennis game launch video
- pm-ultimaxbt-2ddf1e — Food craving launch film
- pm-wani-shola-16ca7a — Developer portfolio site showreel
- pm-gdgtify-287ddf — Speech built as architecture
- pm-koldo2k-5cff87 — Infinite-zoom landscape loop
