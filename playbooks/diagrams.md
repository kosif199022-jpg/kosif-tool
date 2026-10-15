# Diagrams and flows — المخططات والتدفقات

This playbook covers explainer diagrams: nodes and edges revealed in causal order, stroke draw-on, arrows, timelines, architecture and process flows, and camera moves between parts of a diagram. Use it whenever a style's categories include `diagrams`.

يغطي هذا الدليل المخططات الشارحة: عقد وروابط تظهر بترتيب السبب والنتيجة، رسم الخطوط تدريجيًا، الأسهم، الخطوط الزمنية، مخططات البنية والعمليات، وحركة الكاميرا بين أجزاء المخطط.

## 1. When to use — متى تستخدمه

Use a diagram when the viewer must understand a relationship: cause and effect, a sequence, a hierarchy, data flowing through a system, or history along a timeline. If the point is a quantity, use `playbooks/charts.md` instead.

**بالعربية:** استخدم المخطط عندما يجب أن يفهم المشاهد علاقة: سبب ونتيجة، تسلسل، تسلسل هرمي، بيانات تمر في نظام، أو تاريخ على خط زمني. إن كانت الفكرة كمية فاستخدم دليل الرسوم البيانية.

## 2. Visual grammar — القواعد البصرية

- Nodes share one shape family (rounded rectangles r = 16–24 px or circles) and one stroke width (3–4 px at 1080 px).
- At most 7 nodes visible at once; bigger systems are explained in chapters with camera moves.
- Edges are straight or one-bend orthogonal; curves only for feedback loops. Arrowheads 14–18 px.
- Reading direction follows the language: right → left for an Arabic film, left → right for English; time on a timeline flows the same way.
- The active node gets the accent colour; visited nodes return to ink at 70%; future nodes are not drawn yet.
- Labels inside nodes 32–44 px, edge labels 24–28 px placed at the edge midpoint, never crossing a line.

**بالعربية:** شكل موحد للعقد وسماكة خط واحدة. سبع عقد مرئية كحد أقصى. روابط مستقيمة أو بانحناءة واحدة. اتجاه القراءة يتبع اللغة (من اليمين في الفيلم العربي). العقدة النشطة بلون التمييز والسابقة بنسبة 70٪ واللاحقة غير مرسومة بعد.

## 3. Motion mechanics — ميكانيكا الحركة

- Order is causal: a node appears, then its outgoing edge draws, then the next node pops when the pen reaches it.
- Node pop: scale 0.85 → 1 with spring `{ damping: 14, stiffness: 160 }` (~300 ms), opacity in 150 ms.
- Edge draw: `stroke-dashoffset` from path length to 0 at 900–1200 px per second, ease-in-out cubic; the arrowhead fades in during the last 80 ms.
- Data pulse along an edge: a 10–14 px dot travels the path in 600–900 ms with ease-in-out, repeated with 400 ms gaps while the narration describes the flow.
- Camera: pan between chapters in 700–1000 ms with `cubic-bezier(0.65, 0, 0.35, 1)`; zoom 1.0 → 1.4 for detail, never above 1.8. Hold 1.5 s after each move.
- Timeline: the playhead line advances at a constant speed; event markers pop as it reaches them (200 ms), labels follow 120 ms later.

**بالعربية:** الترتيب سببي: عقدة ثم رابطها ثم العقدة التالية عند وصول القلم. ظهور العقدة بنابض حوالي 300 مللي ثانية. رسم الرابط بسرعة 900–1200 بكسل/ثانية. نبضة بيانات على الرابط 600–900 مللي ثانية. تحريك الكاميرا بين الفصول 700–1000 مللي ثانية وتكبير لا يتجاوز 1.8.

## 4. Scene recipes — وصفات المشاهد

**A — Three-step process (عملية من ثلاث خطوات)**

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 300 ms | node 1 pops | spring 14/160 |
| 300 ms | 900 ms | edge 1→2 draws, arrowhead at the end | ease-in-out cubic |
| 900 ms | 1200 ms | node 2 pops, node 1 dims to 70% | spring 14/160 |
| 1200 ms | 1800 ms | edge 2→3 draws | ease-in-out cubic |
| 1800 ms | 2100 ms | node 3 pops in accent | spring 14/160 |
| 2100 ms | 3600 ms | hold; one data pulse runs 1→3 | ease-in-out |

**B — Zoom into a component (التكبير على مكوّن):** whole system at scale 1 (2 s hold), camera moves to one node at scale 1.5 in 900 ms, the node opens into a sub-diagram (cross-fade 300 ms).

**C — Timeline sweep (خط زمني):** the axis draws in 600 ms, the playhead moves at a steady rate, each year marker pops, the current era is highlighted with a band.

**D — Before/after split (قبل وبعد):** the same diagram duplicated; the "after" copy redraws only the changed edges in accent colour.

## 5. Implementation — التنفيذ

Remotion edge draw-on:

```tsx
import { useCurrentFrame, interpolate, Easing } from 'remotion';
export const Edge: React.FC<{ d: string; len: number; from: number; dur: number }> = ({ d, len, from, dur }) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [from, from + dur], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic) });
  return <path d={d} fill="none" stroke="#9fb0cc" strokeWidth={4} strokeDasharray={len} strokeDashoffset={len * (1 - p)} markerEnd={p > 0.95 ? 'url(#arrow)' : undefined} />;
};
```

SVG in the html-canvas starter: give the path `pathLength="1"` and set `style.strokeDashoffset = 1 - KOSIF.prog(t, t0, t1, KOSIF.Ease.inOutCubic)` in `draw(t)`, with `strokeDasharray = 1`. The starter's chart scene uses exactly this.

## 6. Arabic and RTL notes — ملاحظات العربية

Mirror the whole layout for Arabic films: the first node sits on the right and arrows point left. Mirror arrowhead markers too. Keep code identifiers or product names in Latin inside isolated spans.

**بالعربية:** اعكس المخطط كاملًا في الفيلم العربي: العقدة الأولى يمينًا والأسهم نحو اليسار، واعكس رؤوس الأسهم أيضًا.

## 7. Audio sync — المزامنة مع الصوت

Each node pops on the word that names it (within 100 ms). Edges draw during the connecting phrase ("which then sends…"). Camera moves happen in pauses longer than 400 ms, never over a key term.

**بالعربية:** تظهر كل عقدة مع الكلمة التي تسميها، وتُرسم الروابط أثناء العبارة الواصلة، وتتحرك الكاميرا في الوقفات الأطول من 400 مللي ثانية.

## 8. Quality checklist — قائمة الفحص

1. Reveal order matches cause and effect?
2. Seven nodes or fewer on screen?
3. No label crosses a line?
4. Reading direction matches the film language?
5. Arrowheads appear only when edges finish?
6. Camera holds 1.5 s after each move?
7. Node names land on spoken names?
8. One active node at a time?
9. Consistent stroke width?
10. Final frame shows the whole diagram, readable?

## 9. Anti-patterns — أخطاء شائعة

Everything appearing at once; spaghetti curves; glowing neon edges on a white diagram; random 3D tilt; icons instead of labels; camera spinning around a flat diagram; arrows pointing against the reading direction.

**بالعربية:** ظهور كل شيء دفعة واحدة، خطوط متشابكة، توهج بلا سبب، ميلان ثلاثي الأبعاد عشوائي، أيقونات بدل التسميات، وأسهم عكس اتجاه القراءة.

## 10. Related styles — استايلات ذات صلة

- tech-blueprint — رسومات تقنية
- map-journey — رحلة على الخريطة
- infographic — إنفوجرافيك
- documentary-map — خريطة وثائقية
- isometric — عالم أيزومتريك
- pm-yunn260414-60d996 — What is Git explainer
- pm-imthatcarlos-e04bfe — Sherwood agentic hedge fund explainer
- pm-alex-prompter-1ea044 — Animated business explainer
