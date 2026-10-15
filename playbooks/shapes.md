# Shapes and morphing — الأشكال والتحوّل

This playbook covers geometric motion: a shape system, path morphs, squash and stretch, the "one shape never cut" sequence, boolean reveals and grid logic. Use it whenever a style's categories include `shapes`.

يغطي هذا الدليل الحركة الهندسية: نظام أشكال، تحوّل المسارات، الانضغاط والتمدد، تسلسل «شكل واحد بلا قطع»، الكشف بالقص، ومنطق الشبكة.

## 1. When to use — متى تستخدمه

Use shape motion for brand systems, logo stories, abstract explainers, loading and transition design, and any film where one element must carry continuity across scenes.

**بالعربية:** استخدمه لأنظمة الهوية، قصص الشعارات، الشروحات المجردة، الانتقالات، وأي فيلم يحتاج عنصرًا واحدًا يحمل الاستمرارية بين المشاهد.

## 2. Visual grammar — القواعد البصرية

- Pick a base unit (e.g. 24 px) and a grid (8 or 12 columns). Every size and position is a multiple of the unit.
- At most three primitives (circle, rounded square, line) and two colours plus background.
- Corner radii come from one scale (0, 8, 24, 50%). Stroke widths come from one scale (2, 4, 8).
- Negative space is a shape too: keep at least 30% of the frame empty.

**بالعربية:** وحدة أساس وشبكة ثابتة، ثلاثة أشكال أولية كحد أقصى، لونان مع الخلفية، أنصاف أقطار وسماكات من سلّم واحد، و30٪ من الإطار فارغ على الأقل.

## 3. Motion mechanics — ميكانيكا الحركة

- Morphs: 500–800 ms with `cubic-bezier(0.65, 0, 0.35, 1)`. Only morph paths with the same number of points and the same winding; resample both paths to 64–128 points first.
- Squash and stretch: preserve area. On impact scaleY 0.7 / scaleX 1.3 for 80 ms, recover with spring `{ damping: 10, stiffness: 220 }`.
- Anticipation: move 8–12% opposite to the travel direction for 120–180 ms before a fast move.
- Travel: fast moves 250–400 ms ease-in-out quint; arcs, not straight lines, for anything that "jumps".
- One shape never cut: the hero shape survives every transition, changing role (button → card → screen) through morphs and scale; there are no hard cuts while it is on screen.
- Grid snaps: elements settle on grid positions; overshoot is allowed only in springs, and the final frame is exactly on the grid.

**بالعربية:** التحوّل 500–800 مللي ثانية بين مسارين متساويين في عدد النقاط (أعد أخذ العينات إلى 64–128 نقطة). الانضغاط يحفظ المساحة. استباق 8–12٪ قبل الحركة السريعة. الحركة السريعة 250–400 مللي ثانية على قوس. الشكل البطل لا يُقطع أبدًا بل يتحول دوره. كل شيء يستقر على الشبكة.

## 4. Scene recipes — وصفات المشاهد

**A — Dot to logo (نقطة إلى شعار)**

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 400 ms | dot drops in on an arc | ease-in quad |
| 400 ms | 480 ms | squash on landing | linear |
| 480 ms | 800 ms | recover | spring 10/220 |
| 800 ms | 1500 ms | dot morphs into the logo mark | ease-in-out cubic |
| 1500 ms | 1900 ms | wordmark wipes in beside it | ease-out quint |

**B — Boolean reveal (كشف بالقص):** a circle mask grows from the hero shape (700 ms, ease-in-out) and reveals the next scene inside it.

**C — Grid choreography (رقصة الشبكة):** a 4×4 grid of squares rotates 90° in a diagonal wave, 40 ms offset per cell, 400 ms each.

**D — Morph through states (التحوّل عبر الحالات):** button → toggle → card → full screen, 600 ms per step, 900 ms holds.

## 5. Implementation — التنفيذ

Remotion morph with resampled paths (use a library such as `flubber` or precomputed equal-point paths):

```tsx
import { useCurrentFrame, interpolate, Easing } from 'remotion';
// a and b: arrays of [x,y] with the same length (resampled offline)
const toD = (pts: number[][]) => 'M' + pts.map((p) => p.join(' ')).join('L') + 'Z';
export const Morph: React.FC<{ a: number[][]; b: number[][]; from: number; dur: number }> = ({ a, b, from, dur }) => {
  const p = interpolate(useCurrentFrame(), [from, from + dur], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic) });
  const pts = a.map((pa, i) => [pa[0] + (b[i][0] - pa[0]) * p, pa[1] + (b[i][1] - pa[1]) * p]);
  return <path d={toD(pts)} fill="#7ee8d2" />;
};
```

Canvas (html-canvas starter): squash with `ctx.scale(1 + s * 0.3, 1 - s * 0.3)` around the contact point, where `s` comes from `KOSIF.window01(t, hit, hit + 0.08, 0.02, 0.06)`.

## 6. Arabic and RTL notes — ملاحظات العربية

Travel direction in an Arabic film flows right → left. When a shape becomes a container for Arabic text, give it room for diacritics and avoid morphing while text is inside it.

**بالعربية:** اتجاه الحركة في الفيلم العربي من اليمين لليسار، ولا تحوّل شكلًا وفيه نص عربي.

## 7. Audio sync — المزامنة مع الصوت

Impacts land on beats or transients; morphs span a phrase; squash frames coincide with the sound's attack within one frame.

**بالعربية:** الاصطدامات على الإيقاع، والتحولات على امتداد العبارة، والانضغاط مع بداية الصوت بإطار واحد.

## 8. Quality checklist — قائمة الفحص

1. All sizes on the base unit?
2. Morph paths resampled to equal points (no tearing)?
3. Area preserved in squash?
4. Final positions exactly on the grid?
5. Hero shape never cut while on screen?
6. At most three primitives?
7. 30% negative space?
8. Impacts on beats?
9. Arcs for jumps?
10. Loop seams invisible if the film loops?

## 9. Anti-patterns — أخطاء شائعة

Morphing unrelated shapes that tear and twist; elastic bounce on everything; random gradients and glow; dozens of floating blobs; rotation without a reason.

**بالعربية:** تحويل أشكال غير متوافقة فتتمزق، ارتداد مطاطي لكل شيء، تدرجات وتوهج عشوائي، وكتل عائمة بلا معنى.

## 10. Related styles — استايلات ذات صلة

- logo-reveal — كشف شعار
- liquid-morph — أشكال سائلة
- minimal — مينيمال
- morph-charts — تحولات بيانات
- glass-ui — واجهة زجاجية
- pm-ultimaxbt-bbebf5 — Orange dot motion system
- pm-lukasersil-0ed38e — Motion techniques showreel
- pm-demonugc-4c5753 — Morphing UI states loop
