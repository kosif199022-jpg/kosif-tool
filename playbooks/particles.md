# Particles and fields — الجسيمات والحقول

This playbook covers particle systems that mean something: seeded emitters, flow fields, attraction and repulsion, text to particles, and performance budgets, while avoiding the generic glowing-dust look. Use it whenever a style's categories include `particles`.

يغطي هذا الدليل أنظمة الجسيمات ذات المعنى: مصادر مزروعة البذرة، حقول تدفق، جذب وتنافر، تحويل النص إلى جسيمات، وميزانية الأداء، مع تجنب مظهر الغبار المتوهج المكرر.

## 1. When to use — متى تستخدمه

Use particles to show quantity becoming structure (many users forming a logo), energy (a burst on a reveal), flow (data moving), or dissolution (an old idea breaking apart). If particles only decorate the background, remove them.

**بالعربية:** استخدم الجسيمات لتُظهر كثرةً تتحول إلى بنية، أو طاقة لحظة الكشف، أو تدفق بيانات، أو تفكك فكرة قديمة. إن كانت مجرد زينة خلفية فاحذفها.

## 2. Visual grammar — القواعد البصرية

- Two or three particle sizes (e.g. 4, 8, 14 px at 1080 px) and at most two colours.
- Count budget: 150–600 particles on Canvas 2D, up to 20 000 with WebGL points.
- Particles sit behind type and never cross a readable word.
- Density communicates: denser = more, sparser = less; do not fill the frame evenly.

**بالعربية:** حجمان أو ثلاثة ولونان كحد أقصى، 150–600 جسيم في Canvas، وخلف النص دائمًا، والكثافة تحمل معنى.

## 3. Motion mechanics — ميكانيكا الحركة

- Determinism: every random value comes from a seeded PRNG (`KOSIF.rng(seed)`), and positions are computed from `t`, not accumulated per frame. That keeps renders identical and lets you seek anywhere.
- Burst: initial speed 400–1300 px/s, distance `d = speed × easeOutExpo(life)`, gravity 60–150 px/s², lifetime 0.7–1.0 of the burst window, alpha `1 − easeInOutCubic(life)`.
- Flow field: angle = noise(x × 0.0025, y × 0.0025, t × 0.2) × 2π, speed 40–120 px/s; analytic noise (sum of 3 sines) is enough and stays deterministic.
- Gather into a shape: sample target points from the shape (or text rendered to an offscreen canvas), assign each particle a target, move with ease-in-out cubic over 900–1400 ms and a per-particle delay of 0–300 ms.
- Attraction to the cursor or a hero element: force ∝ 1/d², clamped, only used in procedural (seekable) form.

**بالعربية:** كل قيمة عشوائية من مولد مزروع البذرة، والمواقع تُحسب من الزمن لا بالتراكم. الانفجار بسرعة 400–1300 بكسل/ثانية ومنحنى outExpo مع جاذبية خفيفة. حقل التدفق من ضوضاء تحليلية. التجمع في شكل خلال 900–1400 مللي ثانية مع تأخير فردي حتى 300 مللي ثانية.

## 4. Scene recipes — وصفات المشاهد

**A — Reveal burst (انفجار الكشف)**

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 250 ms | hero word scales in | spring 14/150 |
| 50 ms | 3000 ms | 160 seeded particles burst from the centre | outExpo distance |
| 100 ms | 1100 ms | ring expands to frame size and fades | outExpo |

**B — Crowd to logo (حشد إلى شعار):** scattered particles drift in a flow field for 1.5 s, then gather into the logo in 1.2 s, then the solid logo cross-fades over them in 300 ms.

**C — Text dissolve (تفكك النص):** sample the word's pixels, replace the word with particles at the same points, then let them drift up 200 px and fade over 1.5 s.

**D — Data stream (تيار بيانات):** particles travel along an SVG path with offsets, 600 ms per traversal, giving a sense of throughput.

## 5. Implementation — التنفيذ

Canvas (the `starters/html-canvas` burst, seekable):

```js
const rand = KOSIF.rng(20261015);
const parts = Array.from({ length: 160 }, () => ({ a: rand() * Math.PI * 2, sp: 400 + rand() * 900, r: 4 + rand() * 10 }));
function drawBurst(ctx, t, t0, t1, cx, cy) {
  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  if (t < t0 || t > t1) return;
  const life = (t - t0) / (t1 - t0);
  for (const q of parts) {
    const d = KOSIF.Ease.outExpo(life) * q.sp;
    ctx.globalAlpha = 1 - KOSIF.Ease.inOutCubic(life);
    ctx.beginPath(); ctx.arc(cx + Math.cos(q.a) * d, cy + Math.sin(q.a) * d + life * 120, q.r * (1 - life * 0.6), 0, 6.283); ctx.fill();
  }
  ctx.globalAlpha = 1;
}
```

Remotion: generate the particle array with `random(seed)` from `remotion` (deterministic) inside `useMemo`, and compute positions from `useCurrentFrame() / fps` in the same pure way.

## 6. Arabic and RTL notes — ملاحظات العربية

Text-to-particles for Arabic must sample the shaped word rendered by the browser (`ctx.fillText` on an RTL canvas with `direction = 'rtl'`), never letter-by-letter glyphs. Hold the readable word for at least 1 s before dissolving it.

**بالعربية:** عند تحويل كلمة عربية إلى جسيمات خذ العينات من الكلمة المشكّلة كاملة، واترك الكلمة مقروءة ثانية على الأقل قبل تفكيكها.

## 7. Audio sync — المزامنة مع الصوت

Bursts start on transients (within one frame). Flow speed may follow the music's loudness envelope, smoothed over 200 ms. Never let particle motion compete with narration emphasis.

**بالعربية:** الانفجار يبدأ مع ضربة الصوت، وسرعة التدفق قد تتبع شدة الموسيقى بعد تنعيمها.

## 8. Quality checklist — قائمة الفحص

1. Seeded and seekable (same frame twice = same pixels)?
2. Particles never cross readable text?
3. Count within budget, render under 50 ms per frame?
4. Particles carry a meaning stated in PLAN.md?
5. Two colours maximum?
6. Burst starts on a transient?
7. Fades complete before the scene ends?
8. Arabic word sampled as a whole?
9. No even "snow" filling the frame?
10. Final frame clean?

## 9. Anti-patterns — أخطاء شائعة

Endless glowing dust behind every scene (the most common AI-made look); bloom on everything; `Math.random()` per frame (flicker, non-deterministic renders); particles over captions; rainbow colours.

**بالعربية:** غبار متوهج دائم خلف كل مشهد، توهج على كل شيء، `Math.random()` في كل إطار، جسيمات فوق الترجمة، وألوان قوس قزح.

## 10. Related styles — استايلات ذات صلة

- neon-tech — نيون تقني
- pm-blue-clarity-ef56d0 — Particle sphere motion reel
- pm-lukasersil-0ed38e — Motion techniques showreel
- pm-ultimaxbt-bbebf5 — Orange dot motion system
- pm-twoclipping-6dd14e — UGC ad generator promo
- pm-demonugc-4c5753 — Morphing UI states loop
