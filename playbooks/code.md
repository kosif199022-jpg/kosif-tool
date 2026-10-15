# Code-driven and generative motion — الحركة البرمجية والتوليدية

This playbook covers motion written as code: procedural and noise-based systems, code-typing and terminal scenes, generative layouts, deterministic seeds and performance. Use it whenever a style's categories include `code`; in practice every KOSIF film is code, so its determinism rules apply everywhere.

يغطي هذا الدليل الحركة المكتوبة كبرنامج: أنظمة إجرائية وضوضاء، مشاهد كتابة الكود والطرفية، تخطيطات توليدية، بذور حتمية وأداء. قواعد الحتمية فيه تنطبق على كل أفلام KOSIF.

## 1. When to use — متى تستخدمه

Use it for developer tools, AI product films, terminal demos, data art, procedural backgrounds and any piece where the system that generates motion is part of the message.

**بالعربية:** لأدوات المطورين وأفلام منتجات الذكاء الاصطناعي وعروض الطرفية والفن البياني والخلفيات الإجرائية.

## 2. Visual grammar — القواعد البصرية

- Code on screen uses a real monospace font at 28–40 px (1080 px width), at most 14 lines visible, syntax colours from one theme.
- Show code that is plausible and correct; never lorem-ipsum code. Highlight the 1–3 lines that matter.
- Terminal: prompt, command, output; output scrolls in blocks, not character by character.
- Generative patterns obey the same palette and grid as the rest of the film.

**بالعربية:** كود حقيقي بخط ثابت العرض 28–40 بكسل و14 سطرًا كحد أقصى، صحيح ومعقول، مع تمييز السطور المهمة فقط. الطرفية: أمر ثم مخرجات على دفعات.

## 3. Motion mechanics — ميكانيكا الحركة

- Determinism: frame = f(t). No `Math.random()`, no `Date.now()`, no state accumulated across frames. Seed PRNGs (`KOSIF.rng`, Remotion `random(seed)`). `tools/render_html.cjs` can also seed `Math.random` (`--seed`) for legacy pages.
- Typing: 25–45 characters per second with ±20% seeded jitter, a 250–400 ms pause after punctuation, caret blinking at 530 ms. Long code is pasted as a block with a 200 ms fade, not typed.
- Line highlight: background band slides in 250 ms (ease-out cubic), other lines dim to 50%.
- Scrolling: in steps of whole lines, 200–300 ms each, ease-in-out.
- Noise fields: analytic noise (sum of 3–4 sines with prime frequencies) or a seeded simplex; scroll noise through time at 0.1–0.3 units per second for calm motion.
- Performance budget: under 50 ms per frame in the renderer; precompute heavy geometry once.

**بالعربية:** الإطار دالة في الزمن، بلا `Math.random()` ولا `Date.now()` ولا حالة متراكمة. الكتابة 25–45 حرفًا/ثانية مع توقف بعد علامات الترقيم، والكود الطويل يُلصق ككتلة. التمرير بأسطر كاملة. ميزانية أقل من 50 مللي ثانية للإطار.

## 4. Scene recipes — وصفات المشاهد

**A — Command and result (أمر ونتيجة)**

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 300 ms | terminal window scales in from 0.96 | ease-out cubic |
| 300 ms | 1300 ms | command types at 35 cps | seeded jitter |
| 1300 ms | 1600 ms | caret blinks, enter key flash | linear |
| 1600 ms | 2400 ms | output appears in 3 blocks | ease-out |
| 2400 ms | 3000 ms | success line highlighted, camera push 3% | ease-in-out |

**B — Code to UI (من الكود إلى الواجهة):** the editor splits; the right half renders the component the code describes, morphing as lines are highlighted.

**C — Generative backdrop (خلفية توليدية):** a seeded flow-line field at 15% opacity, moving 0.2 units/s behind titles.

**D — Diff reveal (كشف الفرق):** removed lines collapse (red, 250 ms), added lines expand (green, 300 ms), unchanged lines slide.

## 5. Implementation — التنفيذ

Remotion typing with seeded jitter:

```tsx
import { useCurrentFrame, useVideoConfig, random } from 'remotion';
export const Typed: React.FC<{ text: string; cps?: number; from?: number }> = ({ text, cps = 35, from = 0 }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  let t = (f - from) / fps, i = 0;
  while (i < text.length && t > 0) {
    t -= (1 / cps) * (0.8 + random(`k${i}`) * 0.4) + (/[.,;:]/.test(text[i]) ? 0.3 : 0);
    if (t > 0) i++;
  }
  const caret = Math.floor(f / (0.53 * fps)) % 2 === 0;
  return <pre dir="ltr" style={{ fontFamily: 'ui-monospace, monospace', fontSize: 34 }}>{text.slice(0, i)}{caret ? '▍' : ' '}</pre>;
};
```

Canvas: compute the same index from `t` in `draw(t)`; keep the jitter table precomputed from `KOSIF.rng(seed)`.

## 6. Arabic and RTL notes — ملاحظات العربية

Code stays LTR inside an RTL page: wrap it in `dir="ltr"` with `unicode-bidi: isolate`. Arabic comments or strings inside code are fine, but the line direction remains LTR. Arabic captions around the code stay RTL.

**بالعربية:** الكود يبقى من اليسار لليمين داخل صفحة عربية، مع عزله بـ `unicode-bidi: isolate`، والتعليقات العربية حوله تبقى RTL.

## 7. Audio sync — المزامنة مع الصوت

Key clicks are optional and soft (−24 dB); command execution lands on a beat or a narration pause; results appear when the narrator names them.

**بالعربية:** أصوات المفاتيح اختيارية وخافتة، وتنفيذ الأمر على ضربة أو وقفة، والنتائج تظهر عند ذكرها.

## 8. Quality checklist — قائمة الفحص

1. Same frame rendered twice gives identical pixels?
2. No `Math.random`/`Date.now` in frame code?
3. Code correct and plausible?
4. At most 14 lines visible, font ≥ 28 px?
5. Long code pasted, not typed?
6. Important lines highlighted?
7. Code isolated LTR in Arabic films?
8. Frame render time under budget?
9. Theme colours consistent?
10. No fake hacker clichés?

## 9. Anti-patterns — أخطاء شائعة

Matrix rain; green-on-black "hacker" clichés; unreadable tiny code; typing every character of a 60-line file; random jitter that changes every render.

**بالعربية:** مطر الماتريكس، كليشيهات الهاكر، كود صغير غير مقروء، كتابة ملف كامل حرفًا حرفًا، واهتزاز عشوائي يتغير مع كل رندر.

## 10. Related styles — استايلات ذات صلة

- tech-blueprint — رسومات تقنية
- saas-demo — استعراض SaaS
- pm-dale-vaz-cc612a — Sahi trading terminal reveal
- pm-yunn260414-60d996 — What is Git explainer
- pm-ror-fly-9950f1 — Negroni recipe animation
- pm-prasenx-8d9323 — Motion showreel with a fully code-synthesized soundtrack
