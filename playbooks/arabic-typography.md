# Arabic type and RTL in motion — الخط العربي والاتجاه RTL في الحركة

This playbook is mandatory whenever a film contains Arabic text. It covers letter joining and why words are never split, fonts that work, baselines and diacritics, mixed Arabic/Latin/number direction, bidi isolation, line breaking, kashida, and sizes for 9:16 phones.

هذا الدليل إلزامي لأي فيلم فيه نص عربي. يغطي اتصال الحروف ولماذا لا تُفكك الكلمات، الخطوط المناسبة، خط الأساس والتشكيل، اتجاه النص المختلط مع اللاتيني والأرقام، العزل الاتجاهي، كسر الأسطر، الكشيدة، والأحجام المناسبة للهاتف.

## 1. When to use — متى تستخدمه

Always, for any Arabic title, caption, label, lyric or UI text in a KOSIF film.

**بالعربية:** دائمًا، لأي عنوان أو ترجمة أو تسمية أو كلمات أغنية أو نص واجهة بالعربية.

## 2. Visual grammar — القواعد البصرية

- Fonts (open licenses): Cairo, Tajawal, IBM Plex Sans Arabic, Noto Sans Arabic, Noto Kufi Arabic, Noto Naskh Arabic, Readex Pro, Almarai. Load them explicitly and wait for `document.fonts.ready` before rendering.
- Sizes at 1080 px width: captions 56–72 px, titles 96–180 px, labels ≥ 32 px. Arabic needs about 10–15% more size than Latin for the same readability.
- Line height 1.5–1.7 for body and captions, 1.25–1.35 for titles with diacritics allowance.
- Weight: 600–900 for motion titles; thin weights shimmer when moving.
- Alignment: right for paragraphs, centre for titles and captions.

**بالعربية:** خطوط مفتوحة الترخيص: Cairo وTajawal وIBM Plex Sans Arabic وNoto وReadex Pro وAlmarai، وانتظر تحميلها قبل الرندر. الترجمة 56–72 بكسل والعناوين 96–180 بكسل. ارتفاع السطر 1.5–1.7. أوزان 600–900 للعناوين المتحركة. المحاذاة لليمين للفقرات وللوسط للعناوين.

## 3. Motion mechanics — ميكانيكا الحركة

- Never split a word into letters for animation. Arabic letters change shape by position (initial, medial, final, isolated); a `<span>` per letter breaks joining and produces wrong glyphs. Animate whole words, phrases or lines.
- To reveal a word progressively, use a clip-path/mask that wipes right → left across the shaped word (350–600 ms, ease-out quart).
- To emphasise one word, change its colour, weight or scale as a whole.
- Never apply `letter-spacing` to Arabic; it breaks connections. Stretching uses kashida (ـ) only in designed titles, sparingly, and never animated character by character.
- Entrance direction follows reading: slide from right, wipe right → left, list items cascade from the right.

**بالعربية:** لا تفكك الكلمة إلى حروف أبدًا، فالحرف العربي يتغير شكله حسب موقعه. حرّك الكلمة أو العبارة كاملة. للكشف التدريجي استخدم قناعًا يمسح من اليمين لليسار. لا تباعد بين الحروف، والكشيدة باعتدال في العناوين المصممة فقط. الدخول من اليمين.

## 4. Scene recipes — وصفات المشاهد

**A — Word-by-word title (عنوان كلمة كلمة)**

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 400 ms | word 1 (rightmost) rises 50 px into place | ease-out quint |
| 120 ms | 520 ms | word 2 | ease-out quint |
| 240 ms | 640 ms | word 3 | ease-out quint |
| 700 ms | 980 ms | key word turns accent colour, scale 1.08 | spring 12/180 |

**B — Mask wipe line (سطر بقناع ماسح):** `clip-path: inset(0 0 0 100%)` → `inset(0 0 0 0)` over 500 ms so the right side appears first.

**C — Bilingual caption (ترجمة ثنائية اللغة):** Arabic line on top (RTL), English below (LTR, 70% size), each in its own block with its own `dir`.

**D — Number highlight (إبراز رقم):** `<bdi>` around the number so "١٢٨٪" or "128%" keeps correct order inside an Arabic sentence.

## 5. Implementation — التنفيذ

React/Remotion word reveal:

```tsx
export const ArabicTitle: React.FC<{ text: string; frame: number }> = ({ text, frame }) => (
  <h1 dir="rtl" lang="ar" style={{ fontFamily: 'Cairo, sans-serif', fontWeight: 900, fontSize: 140, lineHeight: 1.3, textAlign: 'center' }}>
    {text.split(/\s+/).map((w, i) => {
      const p = Math.min(1, Math.max(0, (frame - i * 4) / 12));
      return <span key={i} style={{ display: 'inline-block', margin: '0 0.15em', opacity: p, transform: `translateY(${(1 - p) * 50}px)` }}>{w}</span>;
    })}
  </h1>
);
```

Canvas: set `ctx.direction = 'rtl'`, `ctx.textAlign = 'right'` and draw whole strings with `fillText`; the browser shapes them. For masks, draw the word to an offscreen canvas and reveal with `ctx.rect` clipping from the right.

## 6. Arabic and RTL notes — ملاحظات العربية

- Mixed text: wrap Latin brand names, code and numbers in `<bdi>` or `unicode-bidi: isolate`.
- Digits: choose Western (0–9) or Arabic-Indic (٠–٩) for the whole film; tabular figures for counters (`font-variant-numeric: tabular-nums`).
- Punctuation: Arabic comma (،), semicolon (؛) and question mark (؟).
- Diacritics: allow 0.15–0.25 em headroom; check they are not clipped by masks.
- Line breaking: break between phrases; never leave a single word on the last line of a title.

**بالعربية:** اعزل الأسماء اللاتينية والأرقام، ووحّد شكل الأرقام في الفيلم، واستخدم علامات الترقيم العربية، واترك مساحة للتشكيل، ولا تترك كلمة وحيدة في آخر سطر العنوان.

## 7. Audio sync — المزامنة مع الصوت

Arabic words in `words.json` are whole words; highlight each as it is spoken, 40–80 ms early. Long words may get a progressive right-to-left fill timed across the word's duration.

**بالعربية:** الكلمات في `words.json` كاملة، وتُضاء قبل نطقها بـ 40–80 مللي ثانية، والكلمة الطويلة قد تمتلئ تدريجيًا من اليمين خلال مدتها.

## 8. Quality checklist — قائمة الفحص

1. No word split into letters anywhere?
2. No letter-spacing on Arabic?
3. Fonts loaded before the first frame?
4. Sizes ≥ 56 px for captions on 9:16?
5. Mixed runs isolated, numbers in the right order?
6. One digit system for the whole film?
7. Diacritics not clipped?
8. Wipes and entrances from the right?
9. Arabic punctuation used?
10. Checked at phone size on a real screenshot?

## 9. Anti-patterns — أخطاء شائعة

Letters flying in one by one (disconnected glyphs); reversed text from fonts or tools without shaping; Latin-style letter-spacing; mirrored Latin words; tiny thin Arabic over busy backgrounds; numbers jumping order inside sentences.

**بالعربية:** حروف تطير منفردة، نص معكوس من أدوات لا تدعم التشكيل، تباعد حروف، كلمات لاتينية معكوسة، نص رفيع صغير فوق خلفية مزدحمة، وأرقام بترتيب خاطئ.

## 10. Related styles — استايلات ذات صلة

- kinetic-arabic — تايبوغرافي عربي
- subtitle-punch — كلمات متحركة
- handwriting-reveal — كتابة يدوية
- typewriter — آلة كتابة
- editorial — مونتاج تحريري
