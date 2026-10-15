# Charts and data stories — الرسوم البيانية وقصص البيانات

This playbook covers animated bars, lines, areas, pies, counters, bar-chart races and chart morphs in KOSIF films: how to move numbers without lying about them. It fixes the visual grammar, timing values and Arabic conventions Claude applies whenever a style's categories include `charts`, and how chart beats lock to narration. Read it after the style's `SKILL.md` and before `PLAN.md`.

يغطي هذا الدليل الأعمدة والخطوط والمساحات والدوائر والعدّادات وسباقات الأعمدة وتحوّلات الرسوم في أفلام KOSIF: كيف تتحرك الأرقام دون أن تكذب. يثبّت القواعد البصرية وقيم التوقيت وأعراف العربية التي يطبقها Claude كلما ضمّت فئات الاستايل `charts`، ويشرح كيف تُقفل ضربات الرسم على التعليق الصوتي. اقرأه بعد `SKILL.md` الخاص بالاستايل وقبل كتابة `PLAN.md`.

## 1. When to use — متى تستخدمه

Use this playbook when numbers carry the film's argument: a growth story, a comparison, a share of a whole, a ranking that changes over time, or one KPI that deserves its own moment. It fits product promos with an analytics panel (clicks, revenue, a rank climbing from 38 to 1), explainer segments that weigh options, and report summaries such as "the quarter in sixty seconds".

Do not use a chart when the number is decoration: if nobody would act differently after seeing it, show the sentence. One chart answers one question; three questions get three charts, not three overlays. Write the insight as one sentence in `PLAN.md` ("sales doubled after March") and build the scene so that sentence is the last thing the eye reads.

**بالعربية:** استخدم الدليل عندما يحمل الرقمُ حجةَ الفيلم: نمو، مقارنة، حصة من كل، ترتيب يتغير مع الزمن، أو مؤشر واحد يستحق لحظته. لا تستخدم الرسم كزينة: إن لم يغيّر الرقم قرار المشاهد فاعرض الجملة بدلًا منه. رسم واحد يجيب عن سؤال واحد. اكتب الخلاصة جملةً واحدة في `PLAN.md` قبل أي حركة، وابنِ المشهد بحيث تكون تلك الجملة آخر ما تقرأه العين.

## 2. Visual grammar — القواعد البصرية

- Bars and areas start at a true zero baseline; a line may start above zero only when the axis prints its range and a break mark is drawn.
- Compared charts share one scale and one unit, printed on the axis or beside the number (٪, ر.س, k), never left to the narration.
- One accent colour carries the insight; context sits in a neutral grey. At most four hues for multiple series; a single series is never a rainbow.
- Chrome (axes, gridlines, legend, ticks) at 20–30% contrast, data marks at full contrast. No perspective, gradients or shadows on data.
- Pies: at most five slices plus "other", sorted by size from 12 o'clock. Slices within five points of each other become a stacked bar; the eye cannot rank close angles.
- Type at 1080 px width: labels at least 28 px, ticks at least 24 px, counters 72–160 px, all with tabular figures so digits do not jitter.
- Value labels ride the bar end; lines are labelled at their end point; a legend appears only when two or more series would collide.
- Highlight hierarchy: one element at 100% opacity, the rest at 35–45%, never two highlights at once.
- Real data gets a source line; invented data is marked "illustrative" inside the frame.
- Portrait (9:16): chart at most 920 px wide and 45% of the frame tall, title above, one-line caption below.

**بالعربية:** الأعمدة والمساحات تبدأ من صفر حقيقي، والرسوم المتقارنة تشترك في مقياس واحد ووحدة مطبوعة. لون تمييز واحد للخلاصة ورمادي محايد للسياق، ولا قوس قزح لسلسلة واحدة. المحاور والشبكة بتباين 20–30٪ والبيانات بتباين كامل، بلا منظور ولا تدرجات ولا ظلال. الدوائر خمس شرائح كحد أقصى مع «أخرى»، مرتبة حسب الحجم من الساعة 12. تسميات الفئات 28 بكسل فأكثر، والعدّادات 72–160 بكسل بأرقام ثابتة العرض. عنصر واحد مميز بنسبة 100٪ وما عداه 35–45٪. البيانات الحقيقية لها سطر مصدر، والمخترعة تُوسم «توضيحية» داخل الإطار.

## 3. Motion mechanics — ميكانيكا الحركة

The golden rule: one eased scalar drives both geometry and number, so bar length, counter and label agree at every frame. A bar that overshoots its truth for 100 ms lies for 100 ms, so bars never use springs.

- Chrome first: axis and gridlines over 250–400 ms with `cubic-bezier(0.33, 1, 0.68, 1)`, gridlines staggered 30 ms bottom-up. Data starts 200 ms after the chrome begins.
- Bars grow in 600–800 ms with `cubic-bezier(0.22, 1, 0.36, 1)`: fast start, long settle, no overshoot. Stagger `min(80, 700 / n)` ms so the whole set lands within about a second.
- Counters ease the value over 700–1000 ms (ease-out cubic), round only for display and show the exact final value on the last frame. Digit flicker, if the style wants it, lasts at most 150 ms.
- Line draw-on: 1000–1400 ms per 1000 px of path, ease-out cubic, so the pen slows where the insight lives. Dots pop as the pen passes with spring `{ damping: 14, stiffness: 160, mass: 0.8 }` (about 250 ms). The area fill fades in over 300 ms after the line finishes.
- Pies: one eased angle sweeps the circle in 900 ms with `cubic-bezier(0.65, 0, 0.35, 1)`; slices are cut from that angle so proportions are true at every frame. Labels appear 120 ms after their slice completes.
- Bar-chart race: periods of 800–1200 ms, values linear between periods, rank swaps ease-in-out over 500 ms, axis maximum rescaling ease-out over 600 ms, period label crossfading 120 ms at the boundary. Ten bars maximum.
- Chart morph: 800–1000 ms ease-in-out; the old axis exits 200 ms before, the new axis or legend enters 200 ms after. Morph only between views of the same dataset.
- Highlight: dim the rest to 35% over 300 ms, pulse the key element once (300 ms up, 500 ms down), hold 1200 ms before the next highlight. Every chart's final state holds at least 1500 ms.
- Camera: push-in at most 4% per scene (about 0.5% per second), pans at most 40 px per second, rotation within ±0.5°, no shake.
- Pills and labels pop with spring `{ damping: 14, stiffness: 120, mass: 1 }`; exits run 200–300 ms, ease-in cubic.

**بالعربية:** قيمة واحدة مُسهَّلة تقود الشكل والرقم معًا؛ العمود الذي يتجاوز قيمته 100 مللي ثانية يكذب 100 مللي ثانية، لذلك لا نوابض على الأعمدة. المحاور أولًا 250–400 مللي ثانية، ثم الأعمدة 600–800 مللي ثانية بمنحنى `cubic-bezier(0.22, 1, 0.36, 1)` وتدرّج 60–90 مللي ثانية. العدّادات 700–1000 مللي ثانية وتصل إلى القيمة النهائية الدقيقة. الخط يُرسم 1000–1400 مللي ثانية لكل 1000 بكسل، والنقاط تقفز بنابض `damping 14, stiffness 160`. الدائرة زاوية واحدة تدور 900 مللي ثانية. سباق الأعمدة: الفترة 800–1200 مللي ثانية، تبديل الترتيب 500 مللي ثانية، عشرة أعمدة كحد أقصى. التحوّل 800–1000 مللي ثانية بين عرضين لنفس البيانات فقط. التمييز: إخفات الباقي إلى 35٪ خلال 300 مللي ثانية ونبضة واحدة. الحالة النهائية تثبت 1500 مللي ثانية على الأقل. الكاميرا: دفع ≤ 4٪ لكل مشهد، بلا اهتزاز.

## 4. Scene recipes — وصفات المشاهد

### Recipe A — Ranked bars with one highlight (الأعمدة المرتبة مع تمييز واحد)

Horizontal bars sorted by value; the narration names one, which stays lit while the rest dim.

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 350 ms | title slides 24 px into place; baseline and ticks fade in | ease-out cubic |
| 200 ms | 1000 ms | bars grow from zero, 80 ms stagger, value labels count with each bar | cubic-bezier(0.22, 1, 0.36, 1) |
| 1200 ms | 1500 ms | other bars dim to 35%, key bar pulses once, annotation line draws | ease-in-out cubic |
| 1500 ms | 3200 ms | hold; camera pushes 2% toward the key bar | linear |
| 3200 ms | 3500 ms | bars shrink to baseline in reverse order, or hard cut on the beat | ease-in cubic |

### Recipe B — Line draw-on with a counter at the pen (خط يُرسم وعدّاد عند القلم)

One series; the counter reads the pen tip; the last point is the insight.

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 400 ms | axes and three gridlines enter, bottom up, 30 ms stagger | ease-out cubic |
| 400 ms | 1700 ms | line draws left to right; dots pop as the pen passes; counter tracks the pen | ease-out cubic / spring 14-160 |
| 1700 ms | 2000 ms | area fill fades to 18% opacity; end-point label and unit appear | ease-out cubic |
| 2000 ms | 2400 ms | insight caption rises under the chart; the end point pulses once | ease-out quint |
| 2400 ms | 4000 ms | hold | — |

### Recipe C — Bar-chart race (سباق الأعمدة)

Ten periods, eight to ten bars, the period label works as the clock.

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 500 ms | period label, axis and the first-period bars settle in place | ease-out cubic |
| 500 ms | 10500 ms | one period per 1000 ms: values move linearly, ranks slide over 500 ms, axis max rescales over 600 ms | linear values / ease-in-out ranks |
| each boundary | +120 ms | period label crossfades to the next value | linear |
| 10500 ms | 11000 ms | race freezes, losers dim to 40%, winner's value settles on its exact figure | ease-out cubic |
| 11000 ms | 12500 ms | hold with the insight caption | — |

### Recipe D — Chart morph, bars to donut (تحوّل الأعمدة إلى دائرة)

The same five values shown first as size, then as share.

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 1000 ms | Recipe A entry without the highlight | as above |
| 1600 ms | 1800 ms | axis, ticks and gridlines fade out; value labels detach and float 12 px | ease-in cubic |
| 1800 ms | 2700 ms | each bar bends into its arc, keeping its colour and its label | cubic-bezier(0.65, 0, 0.35, 1) |
| 2700 ms | 3000 ms | centre total counts in; percent labels replace absolute values | ease-out cubic |
| 3000 ms | 4500 ms | hold; one slice highlighted if the narration names it | — |

KPI tiles reuse Recipe B's counter timing: at most three tiles, each card popping with spring 14-120, counters offset by 600 ms, one tile highlighted at the end.

**بالعربية:** أربع وصفات قابلة لإعادة الاستخدام: أعمدة مرتبة مع تمييز واحد (المحاور 0–350، الأعمدة 200–1000، التمييز 1200–1500، ثبات حتى 3200 مللي ثانية)؛ خط يُرسم وعدّاد يتبع القلم (الرسم 400–1700 ثم تعبئة المساحة ثم العنوان)؛ سباق أعمدة بفترة 1000 مللي ثانية وتبديل ترتيب 500 مللي ثانية ثم تجميد وتمييز الفائز؛ تحوّل الأعمدة إلى دائرة بعد خروج المحاور بـ 200 مللي ثانية. بطاقات المؤشرات تعيد توقيت العدّاد بثلاث بطاقات كحد أقصى بإزاحة 600 مللي ثانية. كل وصفة تنتهي بثبات لا يقل عن 1500 مللي ثانية.

## 5. Implementation — التنفيذ

Both starters share one contract: a pure function of time. In `starters/remotion` time is `useCurrentFrame()` and values come from `interpolate`, `spring` and the `src/easing.ts` helpers (`progress()`, `staggerStart()`). In `starters/html-canvas` the page exposes `window.__kosif = { duration, seek(t) }` and `tools/render_html.cjs` calls `seek` once per frame, so the draw function keeps no hidden state. One JSON dataset, one eased variable feeding both shape and text.

### Remotion / React: staggered bars where bar and number share one scalar

```tsx
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";

type Row = { label: string; value: number };
const easeOutQuint = (t: number) => 1 - Math.pow(1 - t, 5); // ~ cubic-bezier(0.22, 1, 0.36, 1)
const CLAMP = { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: easeOutQuint } as const;

export const Bars: React.FC<{ rows: Row[]; start: number; rtl?: boolean; accent: string }> =
  ({ rows, start, rtl = false, accent }) => {
    const frame = useCurrentFrame();
    const { fps, width } = useVideoConfig();
    const max = Math.max(...rows.map((r) => r.value));
    const grow = Math.round(0.7 * fps);                       // 700 ms per bar
    const step = Math.round(Math.min(80, 700 / rows.length) / 1000 * fps);
    const labelW = 220, track = width - labelW - 200;
    return (
      <svg width={width} height={rows.length * 72} style={{ fontVariantNumeric: "tabular-nums" }}>
        {rows.map((r, i) => {
          const t0 = start + i * step;
          const p = interpolate(frame, [t0, t0 + grow], [0, 1], CLAMP);
          const shown = r.value * p;                           // one scalar for bar AND number
          const w = (shown / max) * track;
          const x = rtl ? width - labelW - w : labelW;         // bars grow toward the left in RTL
          const labelX = rtl ? width - 24 : labelW - 24;
          const valueX = rtl ? x - 14 : x + w + 14;
          return (
            <g key={r.label} transform={`translate(0 ${i * 72})`} fontSize={26} fill="#e8e8e8">
              <text x={labelX} y={44} textAnchor="end">{r.label}</text>
              <rect x={x} y={20} width={w} height={34} rx={6} fill={accent} />
              <text x={valueX} y={44} textAnchor={rtl ? "end" : "start"}>
                {Math.round(shown).toLocaleString(rtl ? "ar-EG" : "en-US")}
              </text>
            </g>
          );
        })}
      </svg>
    );
  };
```

Mount it in a `<Sequence>` inside `Film.tsx`; `start` is the frame of the narration word that introduces the chart (section 7).

### Canvas: deterministic line draw-on with the counter reading the pen tip

```js
// film.js — seek driver contract for tools/render_html.cjs
const DURATION = 6, data = [12, 18, 15, 26, 31, 29, 38, 44];   // true values, one series
const ease = (t) => 1 - Math.pow(1 - t, 3);                      // ease-out cubic
const clamp = (t) => Math.min(1, Math.max(0, t));
const canvas = document.getElementById("film"), ctx = canvas.getContext("2d");

function drawFrame(t) {                                          // pure: depends on t only
  const W = canvas.width, H = canvas.height, pad = 120;
  ctx.clearRect(0, 0, W, H);
  const max = Math.max(...data), stepX = (W - 2 * pad) / (data.length - 1);
  const px = (i) => pad + i * stepX;
  const py = (v) => H - pad - (v / max) * (H - 2 * pad);          // zero baseline, no truncation
  ctx.globalAlpha = ease(clamp((t - 0.2) / 0.4));                 // axis first: 200–600 ms
  ctx.strokeStyle = "#5a5a5a"; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(pad, py(0)); ctx.lineTo(W - pad, py(0)); ctx.stroke();
  const head = ease(clamp((t - 0.6) / 1.2)) * (data.length - 1);  // draw-on: 600–1800 ms
  const i = Math.floor(head), f = head - i;
  const tip = i < data.length - 1 ? data[i] + f * (data[i + 1] - data[i]) : data[i];
  ctx.globalAlpha = 1; ctx.strokeStyle = "#19c37d"; ctx.lineWidth = 6; ctx.lineJoin = "round";
  ctx.beginPath();
  for (let k = 0; k <= i; k++) ctx.lineTo(px(k), py(data[k]));
  if (i < data.length - 1) ctx.lineTo(px(i) + f * stepX, py(tip));
  ctx.stroke();
  ctx.fillStyle = "#ffffff"; ctx.font = "600 72px 'Noto Kufi Arabic', sans-serif";
  ctx.textAlign = "right";                                        // counter = the pen's value
  ctx.fillText(Math.round(tip).toLocaleString("ar-EG"), W - pad, pad);
}

window.__kosif = { duration: DURATION, fps: 30, seek: (t) => drawFrame(t) };
```

Preview with `node tools/render_html.cjs --in film.html --out preview.mp4 --preview`, check the contact sheet at 0.6 s, 1.2 s and 1.8 s, then render with `--audio` when a voice track exists.

**بالعربية:** القالبان يشتركان في عقد واحد: دالة نقية للزمن. في Remotion الزمن هو `useCurrentFrame()` والقيم تُشتق بـ `interpolate` أو `spring`؛ في html-canvas تعرض الصفحة `window.__kosif = { duration, seek(t) }` ويستدعي المحرّك `seek` لكل إطار، فلا حالة مخفية بين الاستدعاءات. احتفظ بالبيانات في كائن JSON واحد، وبالقيمة المُسهَّلة في متغير واحد يغذي الشكل والنص معًا. المقطع الأول أعمدة متدرجة يشترك فيها العمود والرقم في قيمة واحدة مع دعم RTL، والثاني خط يُرسم على Canvas مع عدّاد يقرأ قيمة رأس القلم.

## 6. Arabic and RTL notes — ملاحظات العربية

- Decide the axis direction once and record it in `STYLE.md`. Default: the time axis stays left to right, because dates and digits read that way even inside Arabic text and a mirrored timeline reads as going backwards. Mirror only categorical layouts: horizontal bars take labels on the right and grow leftward; legends list right to left with the swatch on the right.
- One digit system for the whole film (Western 0–9 or Arabic-Indic ٠–٩) on ticks, counters and captions alike. `toLocaleString("ar-EG")` gives Arabic-Indic digits; `"ar-SA"` or `"en-US"` keep Western ones. ٪ and the currency word (ر.س) follow the number.
- Never split an Arabic label into letters; animate the whole word (fade, slide, mask) so shaping stays intact. See `playbooks/arabic-typography.md`.
- Fonts with real Arabic coverage (Noto Kufi Arabic, IBM Plex Sans Arabic, Cairo); `font-variant-numeric: tabular-nums` on counters; line height at least 1.6 for two-line labels.
- Pies sweep clockwise from 12 o'clock unless the whole chart is mirrored; counter-clockwise is not "RTL", only unusual.
- Annotations and arrows start on the right and point left toward the data; the insight caption is right-aligned under the chart.
- Mixed content (Arabic label, Latin product name) needs `dir="rtl"` and `unicode-bidi: isolate` on the container, in SVG `<text>` as in HTML.

**بالعربية:** قرّر اتجاه المحاور مرة واحدة ودوّنه في `STYLE.md`: محور الزمن يبقى من اليسار إلى اليمين افتراضيًا لأن التواريخ والأرقام تُقرأ هكذا، وتُعكس فقط التخطيطات الفئوية (تسميات على اليمين وأعمدة تنمو نحو اليسار، ووسيلة إيضاح من اليمين). نظام أرقام واحد للفيلم كله، وعلامة ٪ بعد الرقم. لا تفكك الكلمة لتحريك حروفها. خطوط عربية حقيقية وأرقام ثابتة العرض للعدّادات. الدائرة تدور مع عقارب الساعة ما لم يُعكس الرسم كله. الأسهم والتعليقات تبدأ من اليمين. النصوص المختلطة تحتاج `dir="rtl"` و `unicode-bidi: isolate`.

## 7. Audio sync — المزامنة مع الصوت

When `words.json` exists it is the master clock; the chart's job is to make each spoken number visible as it is spoken.

- A counter finishes on the start of the word that says the number, within ±100 ms, so it begins 700–1000 ms earlier and is settled when heard. Visuals may lead audio by up to 150 ms, never lag.
- A bar finishes growing at the end of the phrase that names it; the highlight pulse lands on the `emphasis: true` word. A scene's first word in `words.json` is the chart's entry frame and its last word the earliest exit.
- A line draw-on spans the sentence describing the trend: start on its first word, reach the end point as the last word begins, caption in the pause after it.
- With music only, align staggers to beat subdivisions (120 BPM gives a 500 ms beat; stagger 125 or 250 ms), rank swaps to the bar and the final hold to a downbeat. Cut on the beat, never mid-count.
- With no audio, use the timings of section 3 and hold 1500 ms after each insight.
- In `TEST_REPORT.md` list every spoken number, its word start and the frame where the counter shows that exact value; the gap must be within 3 frames at 30 fps.

**بالعربية:** عند وجود `words.json` فهو الساعة الرئيسية. العدّاد ينتهي عند بداية الكلمة التي تنطق الرقم بفارق ±100 مللي ثانية، ويبدأ قبلها بـ 700–1000 مللي ثانية. نمو العمود ينتهي مع نهاية العبارة التي تسمّيه، ونبضة التمييز تقع على كلمة `emphasis`. الخط يُرسم على امتداد جملة الاتجاه. مع الموسيقى بلا صوت: التدرّج على تقسيمات الإيقاع والقطع على الضربة. بلا صوت: توقيتات القسم 3 مع ثبات 1500 مللي ثانية بعد كل خلاصة. وثّق في `TEST_REPORT.md` كل رقم منطوق وإطار ظهوره بفارق لا يتجاوز 3 إطارات.

## 8. Quality checklist — قائمة الفحص

1. Do bars and areas start at zero, with any cut axis marked by a visible break? (yes/no)
2. Do bar length, counter and label agree at every frame, with no overshoot? (yes/no)
3. Does every counter end on its exact final value? (yes/no)
4. Is only one element highlighted at a time, the rest dimmed to 35–45%? (yes/no)
5. Do compared charts share a scale and print their unit inside the frame? (yes/no)
6. Does each chart's final state hold at least 1500 ms before the exit? (yes/no)
7. Do axes, gridlines and legend enter before the data, at 20–30% contrast? (yes/no)
8. Is the axis direction recorded in `STYLE.md` and consistent across scenes? (yes/no)
9. Do spoken numbers appear within ±100 ms of their word in `words.json`, logged in `TEST_REPORT.md`? (yes/no)
10. Are Arabic labels whole words with intact shaping, one digit system and tabular figures? (yes/no)

**بالعربية:** عشرة فحوص بنعم أو لا: صفر حقيقي أو كسر محور مرئي؛ العمود والعدّاد والتسمية بقيمة واحدة بلا تجاوز؛ العدّاد يصل إلى القيمة الدقيقة؛ تمييز واحد فقط في كل لحظة؛ مقياس ووحدة مشتركة للرسوم المتقارنة؛ ثبات 1500 مللي ثانية؛ المحاور قبل البيانات وبتباين منخفض؛ اتجاه المحاور موثّق في `STYLE.md`؛ الأرقام المنطوقة ضمن ±100 مللي ثانية وموثّقة في `TEST_REPORT.md`؛ العربية كلمات كاملة بنظام أرقام واحد.

## 9. Anti-patterns — أخطاء شائعة

The tells of a generic AI-generated data scene:

- Bouncing bars: a spring on bar length overshoots the value; the chart lies for a few frames and the viewer feels it.
- Everything-animates soup: title, axes, bars, labels, legend and a particle burst entering at once from different directions; nothing is readable, so nothing is believed.
- Slot-machine counters flickering random digits for a second, then snapping to the result.
- Neon glow, gradient fills, drop shadows and 3D tilt on data marks; rainbow bars for a single series.
- Invented "Q1 Q2 Q3" values when the brief contained real figures, or a chart with no unit, axis or source.
- A truncated y-axis turning a two-percent change into a cliff, with no break mark.
- Morphing into a pie of a different dataset because the transition looked nice; the viewer assumes a continuity that is not there.
- Idle wobble or floating on a chart that should be holding; a chart at rest can be read.
- Chart and caption landing simultaneously; the chart lands first, the caption follows.
- Camera shake, handheld drift or fast push-ins on tabular information.
- Mirrored time axes, disconnected Arabic letters, Western and Arabic-Indic digits mixed in one frame.

**بالعربية:** علامات «المظهر الآلي»: أعمدة ترتد بنابض فتتجاوز قيمتها؛ كل شيء يدخل دفعة واحدة من اتجاهات مختلفة؛ عدّادات تومض بأرقام عشوائية ثم تقفز إلى النتيجة؛ توهج نيون وتدرجات وظلال ومنظور ثلاثي الأبعاد وقوس قزح لسلسلة واحدة؛ بيانات مخترعة بدل أرقام المستخدم الحقيقية أو رسم بلا وحدة ولا مصدر؛ محور مقطوع يحوّل 2٪ إلى هاوية؛ تحوّل بين بيانات مختلفة؛ اهتزاز خامل أثناء الثبات؛ الرسم والعنوان في اللحظة نفسها؛ اهتزاز كاميرا على معلومات جدولية؛ محور زمن معكوس أو حروف عربية مفككة أو خلط نظامي الأرقام.

## 10. Related styles — استايلات ذات صلة

- chart-race — سباق رسوم
- morph-charts — تحولات بيانات
- infographic — إنفوجرافيك
- pm-steventey-0d20e4 — Dub promo video
- pm-utopyaszx-1b2f94 — Bold Pilot SEO promo
- pm-ceowinkz-7c776b — Amazon wholesale pitch video
- pm-palashbagchi11-0a4b6b — Backlink audit data promo
- pm-daniel-haida-8691d4 — Taxtello bookkeeping app film
