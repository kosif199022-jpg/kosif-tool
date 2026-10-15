# Hand-drawn, whiteboard and plotter — الرسم اليدوي والسبورة والبلوتر

This playbook covers drawn-looking films: stroke draw-on order, pen and hand overlays, whiteboard and chalkboard explainer rhythm, doodle imperfection, plotter aesthetics and paper textures. Use it whenever a style's categories include `hand-drawn`.

يغطي هذا الدليل الأفلام ذات المظهر المرسوم: ترتيب رسم الخطوط، اليد والقلم، إيقاع شروحات السبورة البيضاء والطباشير، عفوية الدودل، جمالية البلوتر وخامات الورق.

## 1. When to use — متى تستخدمه

Use for educational explainers, storytelling with a warm human feel, sketches that become products, and process films. It lowers perceived complexity; avoid it for luxury or high-tech brands unless contrasted on purpose.

**بالعربية:** للشروحات التعليمية والقصص الدافئة والرسومات التي تتحول إلى منتج. يقلل الإحساس بالتعقيد؛ تجنّبه للعلامات الفاخرة إلا عن قصد.

## 2. Visual grammar — القواعد البصرية

- One pen weight family (e.g. 4 and 8 px), one ink colour plus one highlight colour; chalkboard inverts it.
- Strokes are slightly imperfect: 1–2 px wobble, rounded caps, overshoot at corners.
- Drawings are built from few strokes (5–30 per object) so draw-on reads clearly.
- Paper/board texture at 5–10% opacity, static (never boiling unless the style asks for it).

**بالعربية:** سماكتان للقلم، حبر واحد ولون تمييز واحد، خطوط غير مثالية قليلًا، عناصر من 5–30 خطًا، وخامة ورق ثابتة بنسبة 5–10٪.

## 3. Motion mechanics — ميكانيكا الحركة

- Draw order follows how a person draws: outline first, then details, then fill/hatching; left-to-right for English, right-to-left for Arabic writing.
- Pen speed 800–1400 px/s along the path with ease-in-out per stroke; 60–120 ms lift between strokes.
- Fills appear after the outline: hatching drawn at 2000 px/s or a 300 ms wipe.
- Hand overlay: the hand's pen tip is pinned to the current path point; the hand lags 1 frame and rotates ±5° with the stroke direction. Remove the hand during holds.
- Boil (line jitter) for doodle looks: swap 3 slightly different stroke versions every 2–3 frames (on twos).
- Whiteboard rhythm: draw while the narrator explains, hold 1.5–2 s when the sentence completes, then pan or wipe to clean board space.
- Plotter: constant pen speed (no easing), visible pen-up travel as thin lines at 10% if desired.

**بالعربية:** ترتيب الرسم كما يرسم الإنسان: المحيط ثم التفاصيل ثم التظليل، ومن اليمين للكتابة العربية. سرعة القلم 800–1400 بكسل/ثانية. اليد مثبتة على رأس الخط وتُزال أثناء الثبات. الارتعاش بتبديل 3 نسخ من الخط كل إطارين أو ثلاثة. البلوتر بسرعة ثابتة.

## 4. Scene recipes — وصفات المشاهد

**A — Draw and label (ارسم وسمِّ)**

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 900 ms | object outline draws | ease-in-out per stroke |
| 900 ms | 1300 ms | details | ease-in-out |
| 1300 ms | 1600 ms | highlight fill wipes in | ease-out |
| 1600 ms | 2300 ms | handwritten label writes beside it | constant |
| 2300 ms | 4000 ms | hold, hand leaves frame | ease-in |

**B — Whiteboard pan (تحريك السبورة):** the camera slides 1 board-width in 800 ms (ease-in-out) to fresh space, keeping the previous drawing partially visible.

**C — Sketch to real (من الرسم إلى الحقيقي):** a pencil sketch of a UI draws, then cross-fades (400 ms) into the real screenshot at the same geometry.

**D — Chalkboard formula (معادلة على السبورة):** chalk strokes with dusty texture, each term pops a small chalk-dust puff on completion.

## 5. Implementation — التنفيذ

Remotion stroke draw-on with a pen tip:

```tsx
import { useCurrentFrame, interpolate } from 'remotion';
import { useEffect, useRef, useState } from 'react';
export const DrawnPath: React.FC<{ d: string; from: number; dur: number }> = ({ d, from, dur }) => {
  const ref = useRef<SVGPathElement>(null); const [len, setLen] = useState(1);
  useEffect(() => { if (ref.current) setLen(ref.current.getTotalLength()); }, [d]);
  const p = interpolate(useCurrentFrame(), [from, from + dur], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const tip = ref.current?.getPointAtLength(len * p);
  return (<>
    <path ref={ref} d={d} fill="none" stroke="#1d2433" strokeWidth={6} strokeLinecap="round" strokeDasharray={len} strokeDashoffset={len * (1 - p)} />
    {tip && p > 0 && p < 1 && <circle cx={tip.x} cy={tip.y} r={5} fill="#1d2433" />}
  </>);
};
```

In the html-canvas starter use `pathLength="1"` with `strokeDashoffset`, and place a hand image at `path.getPointAtLength(p * path.getTotalLength())`.

## 6. Arabic and RTL notes — ملاحظات العربية

Handwritten Arabic must be real handwriting or a handwriting-style Arabic font revealed by a right-to-left mask over whole words; never draw Arabic as disconnected letter strokes. The hand moves right to left.

**بالعربية:** الخط اليدوي العربي يكون كتابة حقيقية أو خطًا يدويًا يُكشف بقناع من اليمين لليسار على كلمات كاملة، ولا يُرسم كحروف منفصلة، واليد تتحرك من اليمين.

## 7. Audio sync — المزامنة مع الصوت

Each object finishes drawing as its name is spoken; holds match sentence ends; soft marker or chalk sounds (−22 dB) only during drawing.

**بالعربية:** يكتمل رسم كل عنصر عند ذكر اسمه، والثبات مع نهاية الجملة، وصوت القلم خافت أثناء الرسم فقط.

## 8. Quality checklist — قائمة الفحص

1. Draw order natural (outline → detail → fill)?
2. Pen speed consistent across the film?
3. Hand tip pinned to the stroke?
4. Hand removed during holds?
5. Arabic writing whole words, right to left?
6. Texture static and subtle?
7. Objects finish on their spoken names?
8. Clean space before each new idea?
9. Line weights from one family?
10. Final board readable as a summary?

## 9. Anti-patterns — أخطاء شائعة

Drawing everything at the same time; perfect vector lines pretending to be hand-drawn; a hand floating away from the line; constant boiling on all lines; clip-art icons dropped into a drawn world.

**بالعربية:** رسم كل شيء في وقت واحد، خطوط مثالية تدّعي أنها يدوية، يد بعيدة عن الخط، ارتعاش دائم، وأيقونات جاهزة وسط عالم مرسوم.

## 10. Related styles — استايلات ذات صلة

- whiteboard — سبورة بيضاء
- whiteboard-cinematic — وايتبورد سينمائي
- chalkboard — سبورة طباشير
- doodle — قصص الدودل
- plotter — قلم البلوتر
- handwriting-reveal — كتابة يدوية
- cutout-paper — قصاصات ورقية
- pm-abderrahmen-g-9e8ed0 — Sketchbook animals come alive
