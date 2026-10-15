# Characters and rigs — الشخصيات والهياكل

This playbook covers character animation in KOSIF films: model sheets, simple 2D/SVG rigs, key poses, anticipation and follow-through, walk cycles, mouth shapes and expressions, from stickmen to clay-like and anime-inspired looks. All designs must be original. Use it whenever a style's categories include `characters`.

يغطي هذا الدليل تحريك الشخصيات: أوراق تصميم الشخصية، هياكل ثنائية الأبعاد بسيطة، الوضعيات المفتاحية، الاستباق والمتابعة، دورات المشي، أشكال الفم والتعابير، من الشخصيات العصوية إلى مظهر الصلصال والأنمي. كل التصاميم يجب أن تكون أصلية.

## 1. When to use — متى تستخدمه

Use a character when the story needs empathy or a point of view: a user facing a problem, a guide explaining a process, a mascot reacting to results. Never imitate an existing franchise character or a real person's likeness without permission.

**بالعربية:** استخدم الشخصية عندما تحتاج القصة تعاطفًا أو وجهة نظر. لا تقلّد شخصية من عمل قائم ولا ملامح شخص حقيقي دون إذن.

## 2. Visual grammar — القواعد البصرية

- Write a model sheet in STYLE.md first: proportions (heads tall), palette (3–5 colours), line weight, front/side/three-quarter views.
- Silhouette test: every key pose must read as a solid black shape.
- Simple rigs: head, torso, upper/lower arm, hand, upper/lower leg, foot as separate SVG groups with explicit pivot points.
- Faces: eyes and mouth are swapped shapes, not distorted paths; 5–7 mouth shapes cover speech.

**بالعربية:** اكتب ورقة تصميم في STYLE.md: النسب، 3–5 ألوان، سماكة الخط، الزوايا. كل وضعية مفتاحية تُقرأ كظل أسود. هيكل من مجموعات SVG لكل جزء مع نقطة دوران واضحة. أشكال الفم 5–7 تبادليًا.

## 3. Motion mechanics — ميكانيكا الحركة

- Pose to pose: block key poses first (every 8–16 frames at 24–30 fps), then add breakdowns.
- Anticipation: 4–8 frames opposite to the action; follow-through: hair, clothes, accessories lag 2–4 frames and overshoot 5–10%.
- Arcs: hands and heads move on arcs; rotation easing ease-in-out sine.
- Walk cycle: 24 frames per two steps at 24 fps (12 per step); contact, down, passing, up; body bobs 3–5% of height.
- Holds: a "moving hold" keeps 1–2% breathing scale on the torso over 2 s so the character never freezes.
- Animating on twos (12 drawings per second) suits hand-drawn and stop-motion looks; on ones for smooth vector.
- Lip-flap: switch mouth shape within 1 frame of the phoneme; closed mouth on M/B/P.

**بالعربية:** ابنِ الوضعيات المفتاحية أولًا ثم الوسطيات. استباق 4–8 إطارات ومتابعة متأخرة 2–4 إطارات. الحركة على أقواس. دورة المشي 12 إطارًا للخطوة. تنفّس خفيف 1–2٪ أثناء الثبات. حرّك على «اثنين» لمظهر اليدوي والستوب موشن. الفم يتبدل خلال إطار من الصوت.

## 4. Scene recipes — وصفات المشاهد

**A — Reaction beat (لحظة رد الفعل)**

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 200 ms | anticipation: character sinks 4% | ease-in sine |
| 200 ms | 450 ms | jumps up, arms out | ease-out cubic |
| 450 ms | 700 ms | lands, squash 8% | spring 12/200 |
| 450 ms | 800 ms | hair/scarf follow-through | ease-out |
| 800 ms | 2000 ms | moving hold with smile | sine breathing |

**B — Walk across frame (عبور الإطار):** cycle in place while the background parallax moves at the stride speed (stride length / 0.5 s).

**C — Talk to camera (الحديث للكاميرا):** head tilts ±3° on stressed words, blinks every 2.5–4 s (3-frame blink), mouth shapes from the phoneme timing.

**D — Point and reveal (الإشارة والكشف):** the arm extends on an arc in 350 ms, the target element pops 80 ms after the finger stops.

## 5. Implementation — التنفيذ

Remotion rig rotation:

```tsx
import { useCurrentFrame, interpolate, Easing } from 'remotion';
export const Arm: React.FC = () => {
  const f = useCurrentFrame();
  const shoulder = interpolate(f, [0, 6, 14, 24], [0, 8, -55, -48], { extrapolateRight: 'clamp', easing: Easing.inOut(Easing.sin) });
  const elbow = interpolate(f, [2, 10, 18, 26], [0, 5, -30, -24], { extrapolateRight: 'clamp', easing: Easing.inOut(Easing.sin) });
  return (
    <g transform={`rotate(${shoulder} 200 300)`}>
      <rect x={190} y={300} width={20} height={90} rx={10} fill="#f3c9a0" />
      <g transform={`rotate(${elbow} 200 390)`}><rect x={192} y={390} width={16} height={80} rx={8} fill="#f3c9a0" /></g>
    </g>
  );
};
```

The elbow keys start 2 frames after the shoulder: that offset is the follow-through. In the html-canvas starter, set `transform` on nested `<g>` elements from `KOSIF.prog` values in `draw(t)`.

## 6. Arabic and RTL notes — ملاحظات العربية

In Arabic films characters enter from the right and look left toward the reading direction. Speech bubbles hold whole Arabic phrases with RTL alignment; leave room for diacritics.

**بالعربية:** في الفيلم العربي تدخل الشخصية من اليمين وتنظر نحو اليسار، وفقاعات الكلام تحمل عبارات كاملة بمحاذاة يمين.

## 7. Audio sync — المزامنة مع الصوت

Lip shapes follow phoneme or word timing from `words.json`; gestures land 2–4 frames before the stressed word (the body leads the voice); sound effects hit on contact frames.

**بالعربية:** أشكال الفم تتبع توقيت الكلمات، والإيماءة تسبق الكلمة المنبورة بـ 2–4 إطارات، والمؤثرات على إطار الملامسة.

## 8. Quality checklist — قائمة الفحص

1. Original design with a model sheet in STYLE.md?
2. Key poses readable as silhouettes?
3. Anticipation before every big action?
4. Follow-through on secondary parts?
5. Movement on arcs?
6. No frozen holds?
7. Mouth closed on M/B/P?
8. Proportions consistent across scenes?
9. Character enters from the reading side?
10. No likeness of real people or existing characters?

## 9. Anti-patterns — أخطاء شائعة

Puppet-like rotation of the whole body; limbs stretching like rubber unintentionally; identical timing on every part (no overlap); characters sliding instead of walking; imitating famous characters.

**بالعربية:** دوران الجسم ككتلة واحدة، أطراف تتمدد كالمطاط، نفس التوقيت لكل الأجزاء، انزلاق بدل المشي، وتقليد شخصيات مشهورة.

## 10. Related styles — استايلات ذات صلة

- stickman — شخصيات عصوية
- character-rig — تحريك هيكلي
- claymation — صلصال متحرك
- anime-action — أنمي أكشن
- pixel-art — بيكسل آرت
- comics-panels — لوحات كوميكس
- pm-abderrahmen-g-9e8ed0 — Sketchbook animals come alive
- pm-mandelduck-95fd08 — Starry Night cat-spotting game
