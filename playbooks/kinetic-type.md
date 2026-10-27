# Kinetic typography — التايبوغرافي الحركي

This playbook fixes how words move in KOSIF films: timing per word and per line, emphasis beats, masks and wipes, and readability on a phone. Use it whenever a style's categories include `kinetic-type`, and read `playbooks/arabic-typography.md` alongside it for any Arabic text.

يحدد هذا الدليل كيف تتحرك الكلمات في أفلام KOSIF: توقيت الكلمة والسطر، ضربات التأكيد، الأقنعة والمسح، ووضوح القراءة على الهاتف. استخدمه كلما ضمّت فئات الاستايل `kinetic-type`، واقرأ معه `playbooks/arabic-typography.md` لأي نص عربي.

## 1. When to use — متى تستخدمه

Use kinetic type when the words are the content: quotes, hooks, manifestos, narration-led explainers, lyric and poem films, captions that carry the story. Do not animate type that only labels something; labels enter once and stay still.

**بالعربية:** استخدمه عندما تكون الكلمات هي المحتوى: اقتباس، افتتاحية جاذبة، بيان، شرح يقوده التعليق، قصيدة أو أغنية. لا تحرّك نصًا وظيفته تسمية عنصر؛ التسميات تدخل مرة وتثبت.

## 2. Visual grammar — القواعد البصرية

- One idea per screen; at most 7 words visible on a 9:16 frame, 12 on 16:9.
- Two type sizes per scene: the hero word (120–220 px at 1080 px width) and supporting words (56–80 px). A third size is a smell.
- One accent colour marks the emphasis word; everything else is the ink colour.
- Line length 14–22 characters in portrait. Break lines at phrase boundaries, never inside a phrase.
- Safe area: 60 px sides, 120 px top, 220 px bottom (captions and platform UI live there).
- Weight carries emphasis better than scale; jump from 500 to 900 rather than scaling past 1.3×.

**بالعربية:** فكرة واحدة لكل شاشة وسبع كلمات كحد أقصى في 9:16. حجمان فقط: الكلمة البطلة 120–220 بكسل والكلمات الداعمة 56–80 بكسل. لون تمييز واحد لكلمة التأكيد. السطر 14–22 حرفًا ويُكسر عند حدود العبارة. هوامش آمنة 60 جانبًا و120 أعلى و220 أسفل. الوزن أفضل من التكبير للتأكيد.

## 3. Motion mechanics — ميكانيكا الحركة

- Word entrance: 300–450 ms, translateY 40–70 px → 0 with `cubic-bezier(0.22, 1, 0.36, 1)`, opacity 0 → 1 in the first 60% of that time.
- Stagger between words: 70–120 ms when not tied to speech; when tied to speech, each word starts at its `start` from `words.json` minus 60 ms of anticipation.
- Emphasis pop: scale 1 → 1.12 → 1 over 280 ms with spring `{ damping: 12, stiffness: 180 }`, or a weight change 500 → 900 with a 150 ms crossfade.
- Mask reveal: a clip-path wipe of 350–500 ms in the reading direction (right → left for Arabic, left → right for Latin), ease-out quart.
- Line exit: 200–300 ms, ease-in cubic, move 30 px opposite to the entrance. Exits are always shorter than entrances.
- Hold: a line stays fully readable for at least `0.3 s + 0.06 s × characters` after its last word lands.
- Tracking animation: from +0.08 em to 0 over 600 ms for Latin only; never letter-space Arabic.

**بالعربية:** دخول الكلمة 300–450 مللي ثانية بإزاحة 40–70 بكسل ومنحنى `cubic-bezier(0.22, 1, 0.36, 1)`. التدرّج 70–120 مللي ثانية، أو بداية كل كلمة عند توقيتها في `words.json` ناقص 60 مللي ثانية. التأكيد بنبضة 280 مللي ثانية أو تغيير الوزن. القناع يمسح باتجاه القراءة (من اليمين للعربية). الخروج 200–300 مللي ثانية وأقصر دائمًا من الدخول. لا تباعد بين الحروف العربية أبدًا.

- **Hook captions** (each word cuts in blurred and slides 127 px, blur 37.5 → 0 in 20 frames, sharp-start graph; key word bold green with glow; block cuts out together): see `playbooks/overlap-camera.md` section 5.

## 4. Scene recipes — وصفات المشاهد

**A — Hook line (سطر الافتتاح)**

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 120 ms | background flash or cut on the first audio transient | linear |
| 80 ms | 500 ms | words rise in, 90 ms stagger | ease-out quint |
| 500 ms | 780 ms | emphasis word pops and changes to accent colour | spring 12/180 |
| 780 ms | 2000 ms | hold, camera push 2% | linear |

**B — Karaoke caption (ترجمة كاريوكي):** the full phrase is visible at 60% opacity; each word turns 100% with an accent pill at `start`, returns to ink at `end`. Pill scale 0.96 → 1.08 over 140 ms.

**C — Stack and replace (تكديس واستبدال):** three short lines stack downward 120 ms apart; on the next phrase the stack slides up 80 px and the top line exits while the new line enters at the bottom, 350 ms total.

**D — Big word wipe (مسح الكلمة الكبيرة):** a single 200 px word revealed by a clip-path wipe over 450 ms, held 1 s, then wiped out the same direction in 250 ms.

## 5. Implementation — التنفيذ

Remotion (whole words, synced to `words.json`):

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';
type W = { word: string; start: number; end: number };
export const SyncedLine: React.FC<{ words: W[] }> = ({ words }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig(); const t = frame / fps;
  return (
    <div dir="rtl" style={{ display: 'flex', flexWrap: 'wrap', gap: '0 24px', justifyContent: 'center', fontSize: 96, fontWeight: 800 }}>
      {words.map((w, i) => {
        const local = Math.round((w.start - 0.06) * fps);
        const p = spring({ frame: frame - local, fps, config: { damping: 200 }, durationInFrames: 12 });
        const on = t >= w.start && t < w.end;
        return <span key={i} style={{ opacity: p, transform: `translateY(${interpolate(p, [0, 1], [50, 0])}px)`, color: on ? '#7ee8d2' : '#f3f7ff' }}>{w.word}</span>;
      })}
    </div>
  );
};
```

Canvas/DOM (the `starters/html-canvas` pattern): compute each word's progress with `KOSIF.prog(t, w.start - 0.06, w.start + 0.34, KOSIF.Ease.outQuint)` inside `draw(t)` and set `opacity` and `transform` on a `<span>` per word. Never put one `<span>` per Arabic letter.

## 6. Arabic and RTL notes — ملاحظات العربية

Animate whole Arabic words or whole phrases; splitting letters breaks joining. Use `dir="rtl"` on the container and `unicode-bidi: isolate` on Latin or numeric runs. Masks wipe right → left. Keep diacritics inside the line box by adding 0.15 em line-height headroom.

**بالعربية:** حرّك الكلمة العربية كاملة أو العبارة كاملة، فتفكيك الحروف يكسر الاتصال. ضع `dir="rtl"` على الحاوية و`unicode-bidi: isolate` على المقاطع اللاتينية والأرقام. المسح من اليمين لليسار، واترك مساحة 0.15 em للتشكيل.

## 7. Audio sync — المزامنة مع الصوت

Audio is the master clock. Build `words.json` (see `playbooks/audio-sync.md` and `tools/words_convert.py`), start each word 40–80 ms before its spoken onset, and check sync at three timestamps per scene. Emphasis pops land on stressed syllables, not on word starts.

**بالعربية:** الصوت هو الساعة الأساسية. ابدأ كل كلمة قبل نطقها بـ 40–80 مللي ثانية، وافحص التزامن في ثلاث لحظات لكل مشهد، وضع نبضة التأكيد على المقطع المنبور.

## 8. Quality checklist — قائمة الفحص

1. Every line readable at phone size for its full hold time?
2. At most two type sizes per scene?
3. Arabic words whole and joined in every frame?
4. Exits shorter than entrances?
5. Word onsets within 100 ms of speech on key words?
6. Only one accent word per line?
7. Nothing in the bottom 220 px except captions?
8. No line breaks inside a phrase?
9. Numbers isolated with correct direction?
10. Last frame shows a complete, still line?

## 9. Anti-patterns — أخطاء شائعة

Typewriter on every line; letters flying in individually (the generic "AI title" look); glow and chromatic aberration on body text; bouncing every word; text sliding diagonally; random fonts per scene; holding a line shorter than it takes to read.

**بالعربية:** آلة كاتبة لكل سطر، حروف تطير منفردة، توهج على النص، ارتداد كل كلمة، خطوط عشوائية، وإخفاء السطر قبل قراءته.

## 10. Related styles — استايلات ذات صلة

- kinetic-arabic — تايبوغرافي عربي
- subtitle-punch — كلمات متحركة
- typewriter — آلة كتابة
- editorial — مونتاج تحريري
- pm-stephanlivera-df17a2 — Claude motion designer showreel
- pm-steventey-0d20e4 — Dub promo video
- pm-thayto-dev-44b911 — AjustaCV Pro pricing promo
