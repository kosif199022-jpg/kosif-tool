# كتالوج الانتقالات (hyperframes + Remotion TransitionSeries + ffmpeg xfade)

## المعنى قبل الأداة
تلاشٍ متقاطع = «يستمر» · قطع صلب = «استيقظ/تغيّر» · ذوبان بطيء = «انجرف معي» · مسح/دفع = «انتقال مكاني» · تكبير عبر = «ادخل» · حرق/تسريب ضوء = «ذكرى/زمن». نوعان كحد أقصى في الفيلم الواحد.

## القواعد الصلبة (تسبب أخطاء حقيقية إن خولفت)
- المشهد الأول ظاهر افتراضياً؛ المشاهد التالية `opacity:0` على **الحاوية**، والحركة تكشفها.
- الخروج فوق الدخول (z-index أعلى للخارج) في: السقوط، التصغير للخارج، الانقسام القطري.
- تراكبات الكتل المتدرّجة بحجم الإطار الكامل لا شرائح رفيعة؛ تراكب RGB للغليتش بمزج عادي 35% لا multiply (يختفي على الداكن)؛ تسريب الضوء أكبر من الإطار (2400px+) بلا شكل مرئي.
- VHS: استنسخ محتوى المشهد الحقيقي، ونسختان حمراء وزرقاء فوق الشريط الرئيسي، وعشوائية ببذرة ثابتة.
- حرق الصفحة: المحتوى يحترق مع الصفحة بلا حطام؛ إخفاء المشهد بـ `tl.set` لا `onComplete`؛ `clipPath:none` عند الرجوع.
- Clock wipe: مضلّع 9 نقاط بأربعة أرباع في أربع tweens.
- الستائر حسب الطاقة: هادئ 4 أفقي/6 رأسي، متوسط 6-8/8، عالٍ 12-16/16.
- لا تستخدم: iris نجمي، tilt-shift، lens flare بشكل مرئي، hinge/door.

## عائلات CSS/GSAP
| العائلة | الأنواع |
|---|---|
| دفع | push slide، vertical push، elastic push، squeeze |
| شعاعي | circle iris، diamond iris، diagonal split |
| 3D | card flip |
| قياس | zoom through، zoom out |
| ذوبان | crossfade، blur crossfade، focus pull، color dip |
| تغطية | staggered blocks، horizontal/vertical blinds |
| ضوء | light leak، overexposure burn، film burn |
| تشويه | glitch، chromatic aberration، ripple، VHS |
| ميكانيكي | shutter، clock wipe |
| شبكة | grid dissolve (5 ألوان لوحة لا أحادي) |
| أخرى | gravity drop، morph circle، blur through، page burn |

## Remotion
```tsx
<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}><A/></TransitionSeries.Sequence>
  <TransitionSeries.Transition presentation={fade()} timing={linearTiming({durationInFrames: 15})}/>
  <TransitionSeries.Sequence durationInFrames={60}><B/></TransitionSeries.Sequence>
</TransitionSeries>
```
الانتقال يقصّر المدة الكلية (60+60−15=105)؛ الـ Overlay (تسريب ضوء) لا يقصّرها. `springTiming({config:{damping:200}})` للعضوي. الأنواع: fade، slide(direction)، wipe، flip، clockWipe.

## ffmpeg
`xfade=transition=<type>:duration=<d>:offset=<len1-d>` مع `acrossfade=d=<d>`؛ الأنواع في `ffmpeg-recipes.md`.
