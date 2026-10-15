# Ads and product launch films — الإعلانات وأفلام إطلاق المنتجات

This playbook covers short commercial films: the one-second hook, feature beats, price and call-to-action cards, logo reveals, e-commerce product shots, platform pacing and brand consistency. Use it whenever a style's categories include `ads`.

يغطي هذا الدليل الأفلام التجارية القصيرة: جذب الثانية الأولى، ضربات الميزات، بطاقات السعر والدعوة للإجراء، كشف الشعار، لقطات منتجات المتاجر، إيقاع كل منصة، والاتساق مع الهوية.

## 1. When to use — متى تستخدمه

Use for launch videos, app promos, store ads, feature announcements and any film with a commercial goal and a single call to action.

**بالعربية:** لأفلام الإطلاق وإعلانات التطبيقات والمتاجر وإعلانات الميزات وأي فيلم له هدف تجاري ودعوة واحدة للإجراء.

## 2. Visual grammar — القواعد البصرية

- Structure: hook (0–1.5 s) → problem or promise (1.5–4 s) → 2–4 feature beats (2–3 s each) → proof (number, review, demo) → CTA card (2–3 s) → logo (1–1.5 s).
- One message per beat; one CTA per film.
- Brand tokens only: the brand's colours, font and logo, documented in STYLE.md. No invented logos for real companies.
- Product is the hero: at least 40% of frame height in product shots.
- Price/CTA cards: 2 lines maximum, CTA verb first ("حمّل الآن", "Start free").

**بالعربية:** البنية: جذب ثم وعد ثم 2–4 ميزات ثم دليل ثم بطاقة دعوة ثم شعار. رسالة واحدة لكل ضربة ودعوة واحدة للفيلم. ألوان وخط وشعار العلامة فقط. المنتج يشغل 40٪ من ارتفاع الإطار على الأقل.

## 3. Motion mechanics — ميكانيكا الحركة

- Hook: something moves in the very first frame; a cut or major change within 1.5 s. No logo first.
- Feature beats: enter 300–450 ms (ease-out quint), hold until read, exit 200 ms; cut between beats on the music.
- Product hero: slow push 3–5% over the beat, or a 15–30° turn; lighting sweep across the product in 800 ms.
- Price card: number counts up only if it is a saving; otherwise it lands with spring `{ damping: 14, stiffness: 180 }`.
- Logo reveal: 800–1200 ms, built from the brand's own shapes (mask, draw-on or morph), then hold 1 s.
- Platform pacing: TikTok/Reels 9:16, 15–30 s, cuts every 1–2 s; YouTube pre-roll 16:9, key message before 5 s; feed 1:1 or 4:5.

**بالعربية:** يتحرك شيء في الإطار الأول وتغيير كبير قبل 1.5 ثانية، ولا يبدأ الفيلم بالشعار. ضربات الميزات تدخل 300–450 مللي ثانية. المنتج بدفع بطيء 3–5٪. كشف الشعار 800–1200 مللي ثانية من أشكال العلامة نفسها. ريلز وتيك توك 9:16 بقطع كل 1–2 ثانية، ويوتيوب برسالة قبل الثانية الخامسة.

## 4. Scene recipes — وصفات المشاهد

**A — 15-second app ad (إعلان تطبيق 15 ثانية)**

| start | end | action | easing |
|---|---|---|---|
| 0.0 s | 1.5 s | hook: problem sentence slams in, phone slides up | ease-out quint |
| 1.5 s | 4.0 s | feature 1: tap on screen, UI responds | spring 14/160 |
| 4.0 s | 6.5 s | feature 2: chart grows | ease-out quint |
| 6.5 s | 9.0 s | feature 3: notification pops | spring |
| 9.0 s | 11.5 s | proof: rating 4.8 counts up | ease-out cubic |
| 11.5 s | 13.5 s | CTA card | spring 14/180 |
| 13.5 s | 15.0 s | logo reveal and hold | ease-in-out |

**B — Store product (منتج متجر):** product drops on a coloured plinth, turns 30°, three benefit tags pop around it, price lands, CTA.

**C — Before/after (قبل وبعد):** split screen wipes from "before" to "after" in 600 ms, number of saved hours counts.

**D — Logo sting (توقيع الشعار):** brand shape draws on, fills, wordmark wipes in, tagline fades 200 ms later.

## 5. Implementation — التنفيذ

Remotion sequence skeleton:

```tsx
import { Sequence, AbsoluteFill } from 'remotion';
export const Ad: React.FC = () => (
  <AbsoluteFill style={{ background: '#0b1020' }}>
    <Sequence from={0} durationInFrames={45}><Hook /></Sequence>
    <Sequence from={45} durationInFrames={75}><Feature n={1} /></Sequence>
    <Sequence from={120} durationInFrames={75}><Feature n={2} /></Sequence>
    <Sequence from={195} durationInFrames={75}><Feature n={3} /></Sequence>
    <Sequence from={270} durationInFrames={75}><Proof /></Sequence>
    <Sequence from={345} durationInFrames={60}><Cta /></Sequence>
    <Sequence from={405} durationInFrames={45}><Logo /></Sequence>
  </AbsoluteFill>
);
```

In the html-canvas starter the same structure is the `scenes` array with `t0`/`t1` per beat.

## 6. Arabic and RTL notes — ملاحظات العربية

Arabic CTAs use imperative verbs ("اشترك", "حمّل", "اطلب") and Eastern or Western digits consistently (choose one per film). Prices keep currency and number in one isolated span: `<bdi>٤٩ ر.س</bdi>`.

**بالعربية:** الدعوة بفعل أمر، والأرقام موحدة في الفيلم (هندية أو عربية غربية)، والسعر والعملة داخل وسم معزول.

## 7. Audio sync — المزامنة مع الصوت

Cuts on the music grid (see `playbooks/music.md`); voice-over leads each feature; the logo lands on the final musical hit; deliver −14 LUFS.

**بالعربية:** القطع على شبكة الموسيقى، والتعليق يسبق كل ميزة، والشعار على الضربة الأخيرة، والتسليم بجهارة −14 LUFS.

## 8. Quality checklist — قائمة الفحص

1. Motion in the first frame, change before 1.5 s?
2. One message per beat?
3. One CTA, readable for ≥ 2 s?
4. Brand tokens only, documented?
5. Product ≥ 40% frame height in hero shots?
6. Platform aspect and length correct?
7. Works muted (captions or on-screen text)?
8. Prices correct and isolated in Arabic?
9. Logo held ≥ 1 s at the end?
10. Claims truthful and provided by the user?

## 9. Anti-patterns — أخطاء شائعة

Opening with a logo; five messages in one frame; fake reviews or numbers; stock "AI glow" swooshes; CTA shown for less than a second; music that drowns the voice.

**بالعربية:** البدء بالشعار، خمس رسائل في إطار واحد، تقييمات أو أرقام مزيفة، مؤثرات توهج مكررة، دعوة تظهر أقل من ثانية، وموسيقى تغطي الصوت.

## 10. Related styles — استايلات ذات صلة

- product — إعلان إطلاق منتج
- ecommerce-ad — إعلان متجر
- logo-reveal — كشف شعار
- viral-mixed-media — مونتاج مختلط
- neon-tech — نيون تقني
- pm-twoclipping-221cab — Photo print app launch film
- pm-thayto-dev-44b911 — AjustaCV Pro pricing promo
- pm-steventey-0d20e4 — Dub promo video
