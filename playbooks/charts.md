# Charts and data stories — الرسوم البيانية وقصص البيانات

This playbook covers animated bars, lines, areas, pies, counters, bar-chart races and chart morphs in KOSIF films: how to move numbers without lying about them. It fixes the visual grammar, the timing values and the Arabic conventions Claude applies whenever a style's categories include `charts`, and it explains how chart beats lock to narration. Read it after the style's `SKILL.md` and before writing `PLAN.md`.

يغطي هذا الدليل الأعمدة والخطوط والمساحات والدوائر والعدّادات وسباقات الأعمدة وتحوّلات الرسوم في أفلام KOSIF: كيف تتحرك الأرقام دون أن تكذب. يثبّت القواعد البصرية وقيم التوقيت وأعراف العربية التي يطبقها Claude كلما ضمّت فئات الاستايل `charts`، ويشرح كيف تُقفل ضربات الرسم على التعليق الصوتي. اقرأه بعد `SKILL.md` الخاص بالاستايل وقبل كتابة `PLAN.md`.

## 1. When to use — متى تستخدمه

Use this playbook when the film's argument is carried by numbers: a growth story, a comparison between options, a share of a whole, a ranking that changes over time, or one KPI that deserves its own moment. It applies to product promos with an analytics panel (clicks, revenue, a rank climbing from 38 to 1), to explainer segments that weigh choices, and to report summaries such as "the quarter in sixty seconds".

Do not reach for a chart when the number is decoration. If nobody would act differently after seeing it, show the sentence instead. One chart answers one question; a film with three questions gets three charts, not one chart with three overlays. Before animating anything, write the insight as a single sentence in `PLAN.md` ("sales doubled after March") and build the scene so that sentence is the last thing the eye reads.

**بالعربية:** استخدم الدليل عندما يحمل الرقمُ حجةَ الفيلم: نمو، مقارنة، حصة من كل، ترتيب يتغير مع الزمن، أو مؤشر واحد يستحق لحظته. لا تستخدم الرسم كزينة: إن لم يغيّر الرقم قرار المشاهد فاعرض الجملة بدلًا منه. رسم واحد يجيب عن سؤال واحد. اكتب الخلاصة جملةً واحدة في `PLAN.md` قبل أي حركة، وابنِ المشهد بحيث تكون تلك الجملة آخر ما تقرأه العين.

## 2. Visual grammar — القواعد البصرية

- Bars and areas start at a true zero baseline. A line may start above zero only when the axis prints its range and the cut is drawn as a visible break mark.
- Charts that are compared share one scale and one unit. The unit is printed on the axis or beside the number (٪, ر.س, k), never left to the narration.
- One accent colour carries the insight; context sits in a neutral (about 60% grey). A multi-series palette has at most four hues, and a single series never becomes a rainbow.
- Chrome (axes, gridlines, legend, ticks) renders at 20–30% contrast; data marks at full contrast. No perspective, no gradients on data marks, no drop shadows.
- Pies and donuts: at most five slices plus "other", sorted by size, starting at 12 o'clock. When slices are within five points of each other, use a stacked bar instead; the eye cannot rank close angles.
- Type at 1080 px width: category labels at least 28 px, axis ticks at least 24 px, counters 72–160 px, all with tabular figures so digits do not jitter while counting.
- Value labels sit at the end of the bar and travel with it. Direct-label lines at their end point; show a legend only when there are two or more series and direct labelling would collide.
- Highlight hierarchy: the insight element at 100% opacity, everything else at 35–45% while the highlight is on. Only one element is highlighted at a time.
- Real data gets a small source line at the bottom; invented data is marked "illustrative" in the frame, not only in the report.
- Portrait layout (9:16): chart width at most 920 px, chart height at most 45% of the frame, title above, one-line insight caption below.

**بالعربية:** الأعمدة والمساحات تبدأ من صفر حقيقي، والرسوم المتقارنة تشترك في مقياس واحد ووحدة مطبوعة. لون تمييز واحد للخلاصة ورمادي محايد للسياق، ولا قوس قزح لسلسلة واحدة. المحاور والشبكة بتباين 20–30٪ والبيانات بتباين كامل، بلا منظور ولا تدرجات ولا ظلال. الدوائر خمس شرائح كحد أقصى مع «أخرى»، مرتبة حسب الحجم من الساعة 12. تسميات الفئات 28 بكسل فأكثر، والعدّادات 72–160 بكسل بأرقام ثابتة العرض. عنصر واحد مميز بنسبة 100٪ وما عداه 35–45٪. البيانات الحقيقية لها سطر مصدر، والمخترعة تُوسم «توضيحية» داخل الإطار.

## 3. Motion mechanics — ميكانيكا الحركة

The golden rule: one eased scalar drives both the geometry and the number. At every frame the bar length, the counter and the label describe the same value; a bar that overshoots its truth for 100 ms is a 100 ms lie, so bars never use springs.

- Chrome enters first: axis line and gridlines over 250–400 ms with `cubic-bezier(0.33, 1, 0.68, 1)` (ease-out cubic), gridlines staggered 30 ms from the baseline upward, ticks fading in with them. Data starts 200 ms after the chrome begins.
- Bars grow in 600–800 ms with `cubic-bezier(0.22, 1, 0.36, 1)` (ease-out quint): fast start, long settle, no overshoot. Stagger 60–90 ms between bars; for n bars use `min(80, 700 / n)` ms so the whole set lands within about one second.
- Counters run 700–1000 ms on the value with ease-out cubic, rounded only at display time, and show the exact final value on the last frame. A slot-machine digit flicker, if the style asks for it, is limited to the first 150 ms.
- Line draw-on: 1000–1400 ms per 1000 px of path length with ease-out cubic, so the pen slows exactly where the insight lives. Data dots pop as the pen passes them with a Remotion spring `{ damping: 14, stiffness: 160, mass: 0.8 }` (about 250 ms). The area fill fades in over 300 ms after the line has finished, never during the draw.
- Pies: one eased angle sweeps the whole circle in 900 ms with `cubic-bezier(0.65, 0, 0.35, 1)`; slices are cut from that angle so proportions are true at every frame. Slice labels appear 120 ms after their slice completes.
- Bar-chart race: each period lasts 800–1200 ms; values interpolate linearly between periods; rank swaps slide with ease-in-out cubic over 500 ms; the axis maximum rescales with ease-out over 600 ms; the period label snaps at the boundary with a 120 ms crossfade. Ten bars maximum, the leader always fully visible.
- Chart morph (bars to donut, line to bars): 800–1000 ms with ease-in-out; the old axis exits 200 ms before the morph starts and the new axis or legend enters 200 ms after it ends. Morph only between views of the same dataset.
- Highlight: dim the rest to 35% over 300 ms, pulse the key element once (300 ms up, 500 ms down), hold at least 1200 ms before the next highlight. The final state of every chart holds for at least 1500 ms.
- Camera: a push-in of at most 4% per scene (about 0.5% per second), pans at most 40 px per second, rotation within ±0.5°. No shake, no handheld drift on charts.
- Pops for pills and labels use a spring `{ damping: 14, stiffness: 120, mass: 1 }`; exits are shorter than entrances (200–300 ms, ease-in cubic).

**بالعربية:** قيمة واحدة مُسهَّلة تقود الشكل والرقم معًا؛ العمود الذي يتجاوز قيمته 100 مللي ثانية يكذب 100 مللي ثانية، لذلك لا نوابض على الأعمدة. المحاور أولًا 250–400 مللي ثانية، ثم الأعمدة 600–800 مللي ثانية بمنحنى `cubic-bezier(0.22, 1, 0.36, 1)` وتدرّج 60–90 مللي ثانية. العدّادات 700–1000 مللي ثانية وتصل إلى القيمة النهائية الدقيقة. الخط يُرسم 1000–1400 مللي ثانية لكل 1000 بكسل، والنقاط تقفز بنابض `damping 14, stiffness 160`. الدائرة زاوية واحدة تدور 900 مللي ثانية. سباق الأعمدة: الفترة 800–1200 مللي ثانية، تبديل الترتيب 500 مللي ثانية، عشرة أعمدة كحد أقصى. التحوّل 800–1000 مللي ثانية بين عرضين لنفس البيانات فقط. التمييز: إخفات الباقي إلى 35٪ خلال 300 مللي ثانية ونبضة واحدة. الحالة النهائية تثبت 1500 مللي ثانية على الأقل. الكاميرا: دفع ≤ 4٪ لكل مشهد، بلا اهتزاز.

## 4. Scene recipes — وصفات المشاهد

### Recipe A — Ranked bars with one highlight (الأعمدة المرتبة مع تمييز واحد)

Horizontal bars sorted by value, the narration names one of them, that bar stays lit while the rest dim.

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 350 ms | title slides 24 px into place; baseline and ticks fade in | ease-out cubic |
| 200 ms | 1000 ms | bars grow from zero, 80 ms stagger, value labels count with each bar | cubic-bezier(0.22, 1, 0.36, 1) |
| 1200 ms | 1500 ms | non-key bars dim to 35%, key bar pulses once, annotation line draws toward the caption | ease-in-out cubic |
| 1500 ms | 3200 ms | hold; camera pushes 2% toward the key bar | linear |
| 3200 ms | 3500 ms | exit: bars shrink to baseline in reverse order, or hard cut on the beat | ease-in cubic |

### Recipe B — Line draw-on with a counter at the pen (خط يُرسم وعدّاد عند القلم)

One series, the counter reads the value at the pen tip, the last point is the insight.

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
| 10500 ms | 11000 ms | race freezes, losers dim to 40%, winner's value counts to its exact final figure | ease-out cubic |
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

### Recipe E — KPI tiles (بطاقات المؤشرات)

Three counters at most, each with its own beat.

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 300 ms | tile 1 card scales 0.96 to 1 and fades in | spring 14-120 |
| 300 ms | 1100 ms | tile 1 number counts to its value; unit fades in at 900 ms | ease-out cubic |
| 900 ms | 2000 ms | tile 2 repeats the pattern (600 ms offset); tile 3 at 1800 ms | same |
| 2600 ms | 2900 ms | one tile highlighted, the other two dim to 45% | ease-in-out cubic |
| 2900 ms | 4500 ms | hold | — |

**بالعربية:** خمس وصفات قابلة لإعادة الاستخدام: أعمدة مرتبة مع تمييز واحد (المحاور 0–350، الأعمدة 200–1000، التمييز 1200–1500، ثبات حتى 3200 مللي ثانية)؛ خط يُرسم وعدّاد يتبع القلم (الرسم 400–1700 ثم تعبئة المساحة ثم العنوان)؛ سباق أعمدة بفترة 1000 مللي ثانية وتبديل ترتيب 500 مللي ثانية ثم تجميد وتمييز الفائز؛ تحوّل الأعمدة إلى دائرة بعد خروج المحاور بـ 200 مللي ثانية؛ وبطاقات مؤشرات بثلاثة عدّادات بإزاحة 600 مللي ثانية. كل وصفة تنتهي بثبات لا يقل عن 1500 مللي ثانية.

## 5. Implementation — التنفيذ

Both starters share the same contract: a pure function of time. In `starters/remotion` the time is `useCurrentFrame()` and every value is derived with `interpolate` or `spring` from `src/easing.ts` helpers such as `progress()` and `staggerStart()`. In `starters/html-canvas` the page exposes `window.__kosif = { duration, seek(t) }`, and `tools/render_html.cjs` calls `seek` once per frame (the `seek` driver), so the draw function must never keep hidden state between calls. Keep the dataset in one JSON object in `public/` or inline, and keep the eased value in one variable that feeds both the shape and the text.

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

Drop the component into a `<Sequence>` inside `Film.tsx`; `start` is the frame at which the first bar begins, usually the frame of the narration word that introduces the chart (see section 7).

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

Preview with `node tools/render_html.cjs --in film.html --out preview.mp4 --preview`, check the contact sheet at the 0.6 s, 1.2 s and 1.8 s marks, then render with `--audio` when a voice track exists.

**بالعربية:** القالبان يشتركان في عقد واحد: دالة نقية للزمن. في Remotion الزمن هو `useCurrentFrame()` والقيم تُشتق بـ `interpolate` أو `spring`؛ في html-canvas تعرض الصفحة `window.__kosif = { duration, seek(t) }` ويستدعي المحرّك `seek` لكل إطار، فلا حالة مخفية بين الاستدعاءات. احتفظ بالبيانات في كائن JSON واحد، وبالقيمة المُسهَّلة في متغير واحد يغذي الشكل والنص معًا. المقطع الأول أعمدة متدرجة يشترك فيها العمود والرقم في قيمة واحدة مع دعم RTL، والثاني خط يُرسم على Canvas مع عدّاد يقرأ قيمة رأس القلم.

## 6. Arabic and RTL notes — ملاحظات العربية

- Decide the axis direction once and record it in `STYLE.md`. Default: the time axis stays left to right, because dates and digits are read left to right even inside Arabic text, and a mirrored time line reads as "going backwards" to many viewers. Mirror only categorical layouts: horizontal bars take their labels on the right and grow toward the left; legends list right to left with the swatch on the right of the word.
- Choose one digit system for the whole film (Western 0–9 or Arabic-Indic ٠–٩) and apply it to axis ticks, counters and captions alike. `toLocaleString("ar-EG")` gives Arabic-Indic digits and the Arabic thousands separator; `"ar-SA"` or `"en-US"` keep Western digits. The percent sign follows the number (٪ after it) and the currency word follows too (ر.س).
- Never split an Arabic label into letters to animate it; animate the whole word (fade, slide, mask) so shaping stays intact. See `playbooks/arabic-typography.md`.
- Fonts: a Kufi or Naskh family with real Arabic coverage (for example Noto Kufi Arabic, IBM Plex Sans Arabic, Cairo) for labels; set `font-variant-numeric: tabular-nums` on counters so widths do not jump; line height at least 1.6 for two-line labels.
- Pie sweeps stay clockwise from 12 o'clock unless the entire chart is mirrored; a counter-clockwise sweep is not "RTL", it is unusual.
- Annotations and arrows start from the right side of the frame and point left toward the data; the insight caption is right-aligned under the chart.
- Mixed content (Arabic label, Latin product name) needs explicit `dir="rtl"` and `unicode-bidi: isolate` on the label container, in SVG `<text>` as well as in HTML.

**بالعربية:** قرّر اتجاه المحاور مرة واحدة ودوّنه في `STYLE.md`: محور الزمن يبقى من اليسار إلى اليمين افتراضيًا لأن التواريخ والأرقام تُقرأ هكذا، وتُعكس فقط التخطيطات الفئوية (تسميات على اليمين وأعمدة تنمو نحو اليسار، ووسيلة إيضاح من اليمين). نظام أرقام واحد للفيلم كله، وعلامة ٪ بعد الرقم. لا تفكك الكلمة لتحريك حروفها. خطوط عربية حقيقية وأرقام ثابتة العرض للعدّادات. الدائرة تدور مع عقارب الساعة ما لم يُعكس الرسم كله. الأسهم والتعليقات تبدأ من اليمين. النصوص المختلطة تحتاج `dir="rtl"` و `unicode-bidi: isolate`.

## 7. Audio sync — المزامنة مع الصوت

When `words.json` exists it is the master clock, and the chart's job is to make the spoken number visible at the moment it is spoken.

- A counter finishes on the start of the word that says the number, within ±100 ms; begin the count 700–1000 ms before that word so the figure is settled, not still rolling, when the viewer hears it. Visuals may lead audio by up to 150 ms; they must never lag.
- A bar's growth ends on the end of the phrase that names it; the highlight pulse lands on the `emphasis: true` word of the sentence. Entries in `words.json` carry `scene` numbers, so read the first word of a scene as the chart's entry frame and the last word as the earliest frame for an exit.
- A line draw-on spans the sentence that describes the trend: start at its first word, slow to the end point as the last word begins, caption during the pause after it.
- With music and no voice, align bar staggers to beat subdivisions (120 BPM gives a 500 ms beat; stagger at 125 ms or 250 ms), rank swaps in a race to the bar, and the final hold to a downbeat. Cut between charts on the beat, never mid-count.
- With no audio at all, use the fixed timings of section 3 and leave at least 1500 ms of readable hold after each insight.
- Verify in `TEST_REPORT.md`: list every spoken number, its word start from `words.json`, and the frame at which the counter shows that exact value. The difference must be within 3 frames at 30 fps.

**بالعربية:** عند وجود `words.json` فهو الساعة الرئيسية. العدّاد ينتهي عند بداية الكلمة التي تنطق الرقم بفارق ±100 مللي ثانية، ويبدأ قبلها بـ 700–1000 مللي ثانية. نمو العمود ينتهي مع نهاية العبارة التي تسمّيه، ونبضة التمييز تقع على كلمة `emphasis`. الخط يُرسم على امتداد جملة الاتجاه. مع الموسيقى بلا صوت: التدرّج على تقسيمات الإيقاع والقطع على الضربة. بلا صوت: توقيتات القسم 3 مع ثبات 1500 مللي ثانية بعد كل خلاصة. وثّق في `TEST_REPORT.md` كل رقم منطوق وإطار ظهوره بفارق لا يتجاوز 3 إطارات.

## 8. Quality checklist — قائمة الفحص

1. Does every bar and area start from a zero baseline, or is any cut axis marked with a visible break? (yes/no)
2. At every frame, do the bar length, the counter and the label describe the same value, with no overshoot? (yes/no)
3. Does every counter show the exact final value on its last frame, rounded only for display? (yes/no)
4. Is only one element highlighted at any moment, with the rest dimmed to 35–45%? (yes/no)
5. Do compared charts share a scale and print their unit inside the frame? (yes/no)
6. Does the final state of each chart hold for at least 1500 ms before the exit or cut? (yes/no)
7. Do chrome elements (axes, gridlines, legend) enter before data and sit at 20–30% contrast? (yes/no)
8. Is the axis direction decided once, recorded in `STYLE.md`, and consistent across all scenes? (yes/no)
9. Do spoken numbers appear within ±100 ms (3 frames at 30 fps) of their word in `words.json`, and is that logged in `TEST_REPORT.md`? (yes/no)
10. Are Arabic labels whole words with intact shaping, one digit system throughout, and tabular figures on counters? (yes/no)

**بالعربية:** عشرة فحوص بنعم أو لا: صفر حقيقي أو كسر محور مرئي؛ العمود والعدّاد والتسمية بقيمة واحدة بلا تجاوز؛ العدّاد يصل إلى القيمة الدقيقة؛ تمييز واحد فقط في كل لحظة؛ مقياس ووحدة مشتركة للرسوم المتقارنة؛ ثبات 1500 مللي ثانية؛ المحاور قبل البيانات وبتباين منخفض؛ اتجاه المحاور موثّق في `STYLE.md`؛ الأرقام المنطوقة ضمن ±100 مللي ثانية وموثّقة في `TEST_REPORT.md`؛ العربية كلمات كاملة بنظام أرقام واحد.

## 9. Anti-patterns — أخطاء شائعة

These are the tells of a generic AI-generated data scene; each one is avoidable with the numbers above.

- Bouncing bars: a spring on bar length makes the value overshoot and settle; the chart visibly lies for a few frames and the viewer feels it.
- Everything-animates soup: title, axes, bars, labels, legend and a particle burst all entering at once from different directions. Nothing is readable, so nothing is believed.
- Slot-machine counters that flicker random digits for a full second, then snap to the result; the number has no relationship to the motion.
- Neon glow, gradient fills, drop shadows and 3D tilt on data marks; rainbow bars for a single series.
- Invented data standing in for the user's real numbers: "Q1 Q2 Q3" with convenient values when the brief contained actual figures, or a chart with no unit, no axis and no source.
- A truncated y-axis that turns a two-percent change into a cliff, with no break mark and no range on the axis.
- Morphing a bar chart into a pie of a different dataset because the transition looked nice; the viewer assumes continuity that is not there.
- Idle wobble, breathing or floating on charts that are supposed to be holding; a chart at rest is a chart that can be read.
- Chart and caption rendering simultaneously so the eye does not know where to go; the chart lands first, the caption follows.
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
